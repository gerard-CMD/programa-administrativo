import sys
import os
import subprocess
import re
import asteval
import sqlite3
import barcode
import pandas as pd
import fitz 
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image, TableStyle, Spacer, KeepTogether, PageTemplate, Frame
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.units import inch
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
from PyQt5.QtWidgets import QPushButton, QComboBox, QShortcut, QDialog, QSlider, QScrollArea, QApplication, QMainWindow, QMessageBox,QTableWidgetItem, QLabel, QTableWidget, QVBoxLayout, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QCursor, QImage, QPainter
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QRect, QPropertyAnimation, QAbstractAnimation
from ventana_productos_ajuste import InventoryWindowAjuste
from ventana_depositos import VentanaDepositos
import io

class PageNumberCanvas(canvas.Canvas):
    def drawPageNumber(self):
        self.saveState()
        self.setFont("Helvetica", 10)
        self.drawString(500, 10, f"Page {self.getPageNumber()}")
        self.restoreState()

class VentanaPDF(QMainWindow):
    def __init__(self, pdf_buffer):
        super().__init__()
        self.setWindowTitle("Preliminar Cargos de Inventario")
        self.setWindowIcon(QIcon('icono.png'))
        self.setFixedSize(620, 900)

        # Cargar el PDF
        self.pdf_document = fitz.open("pdf", pdf_buffer.read())
        self.current_page = 0  # Página actual
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        # Crear un QScrollArea
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(True)

        # Variables para el movimiento
        self.last_mouse_position = None

        # Control de zoom
        self.zoom_level = 1.0  # Nivel de zoom inicial

        # Botones de navegación
        self.boton_anterior = QPushButton("Anterior", self)
        self.boton_anterior.clicked.connect(self.mostrar_pagina_anterior)

        self.boton_siguiente = QPushButton("Siguiente", self)
        self.boton_siguiente.setGeometry(QtCore.QRect(200, 610, 102, 31))
        self.boton_siguiente.clicked.connect(self.mostrar_pagina_siguiente)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.boton_anterior)
        layout.addWidget(self.boton_siguiente)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Renderizar la primera página del PDF
        self.render_page(self.current_page)

        # Actualizar el estado de los botones
        self.actualizar_botones()

        # Conectar eventos de mouse
        self.label.mousePressEvent = self.mousePressEvent
        self.label.mouseMoveEvent = self.mouseMoveEvent
        self.label.mouseReleaseEvent = self.mouseReleaseEvent

        # Conectar eventos de rueda del mouse
        self.label.wheelEvent = self.wheelEvent

    def wheelEvent(self, event):
        # Ajustar el nivel de zoom según la dirección de la rueda
        if event.angleDelta().y() > 0:
            self.zoom_level += 0.1  # Aumentar zoom
        else:
            self.zoom_level = max(1.0, self.zoom_level - 0.1)  # Disminuir zoom, mínimo 1.0
        self.render_page(self.current_page)  # Volver a renderizar la página con el nuevo zoom

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_mouse_position is not None:
            delta = event.pos() - self.last_mouse_position
            self.label.move(self.label.x() + delta.x(), self.label.y() + delta.y())
            self.last_mouse_position = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_position = None

    def render_page(self, page_number):
        # Renderizar la página como imagen
        page = self.pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom_level, self.zoom_level))  # Aplicar zoom
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(img))

    def actualizar_zoom(self, value):
        self.zoom_level = value  # Actualizar el nivel de zoom
        self.render_page(self.current_page)  # Volver a renderizar la página con el nuevo zoom

    def mostrar_pagina_anterior(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page(self.current_page)
            self.actualizar_botones()

    def mostrar_pagina_siguiente(self):
        if self.current_page < self.pdf_document.page_count - 1:
            self.current_page += 1
            self.render_page(self.current_page)
            self.actualizar_botones()

    def actualizar_botones(self):
        # Deshabilitar el botón "Anterior" si estamos en la primera página
        self.boton_anterior.setEnabled(self.current_page > 0)
        # Deshabilitar el botón "Siguiente" si estamos en la última página
        self.boton_siguiente.setEnabled(self.current_page < self.pdf_document.page_count - 1)

class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Guardar referencia a la ventana principal
        self.setCursor(QCursor(Qt.PointingHandCursor))  # Cambiar el cursor al pasar sobre la imagen

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))  # Cambiar el cursor al pasar sobre la imagen

    def mousePressEvent(self, event):
        # Ejecutar la función preliminar_operacion al hacer clic
        if self.parent:
            self.parent.preliminar_operacion()

class hoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.fuente = self.font()  # Guarda la fuente original
        self.setFont(self.fuente)  # Establece la fuente original al botón
        self.posicionX = 0
        self.posicionY = 0

    def enterEvent(self, event):
        self.posicionX = self.pos().x()
        self.posicionY = self.pos().y()
        
        self.animacionCursor = QPropertyAnimation(self, b"geometry")
        self.animacionCursor.setDuration(100)
        self.animacionCursor.setEndValue(QRect(self.posicionX - 15, self.posicionY - 6, 150, 38))
        self.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)

    def leaveEvent(self, event):
        self.fuente.setPointSize(8)
        
        self.animacionNoCursor = QPropertyAnimation(self, b"geometry")
        self.animacionNoCursor.setDuration(100)
        self.animacionNoCursor.setEndValue(QRect(self.posicionX, self.posicionY, 110, 31))
        self.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)

        # Ajustar el tamaño del botón después de la animación
        self.adjustSize()  # Ajusta el tamaño del botón al contenido

class AjusteProductos(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fila_actual = None  # Inicializa el atributo fila_actual
        self.setupUi(self)
        self.cargar_contador_cargos()
        
        self.contadors_cargo.setText(f"{self.contador_cargos:08d}")  # Muestra el número de cargo con ceros a la izquierda
        
        self.tabla_productos.setCurrentCell(0, 0)
        self.tabla_productos.itemChanged.connect(self.itemChanged)
        self.cargar_deposito_predeterminado()
        
    def setupUi(self, MainWindow):
        self.setFixedSize(1114, 670)

        self.tabla_productos = QtWidgets.QTableWidget(MainWindow)
        self.tabla_productos.setGeometry(QtCore.QRect(60, 190, 1000, 350))
        self.tabla_productos.setStyleSheet("QTableWidget::item:selected {\n"
        "                background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */\n"
        "                color: white; /* Color del texto de la fila seleccionada */\n"
        "            }\n"
        "            QHeaderView::section {\n"
        "                background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */\n"
        "                border: 5px;\n"
        "                color: #ffffff;\n"
        "            }")
        self.tabla_productos.itemChanged.connect(self.moverCursor)
        self.tabla_productos.itemSelectionChanged.connect(self.seleccionarFila)
        self.tabla_productos.cellChanged.connect(self.actualizar_fila_actual)

        self.tabla_productos.setColumnCount(6)
        self.tabla_productos.setRowCount(50)
        self.tabla_productos.verticalHeader().setVisible(False)

        # Configuración de las cabeceras
        for i in range(6):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setFamily("Montserrat SemiBold")
            item.setFont(font)
            self.tabla_productos.setHorizontalHeaderItem(i, item)

        # Establecer el ancho de las columnas
        self.tabla_productos.setColumnWidth(0, 140)
        self.tabla_productos.setColumnWidth(1, 540)
        self.tabla_productos.setColumnWidth(2, 40)
        self.tabla_productos.setColumnWidth(3, 60)
        
        # Hacer que las columnas sean editables o no
        for row in range(100):
            item_cant = QtWidgets.QTableWidgetItem()
            item_cant.setFlags(item_cant.flags() | QtCore.Qt.ItemIsEditable)
            self.tabla_productos.setItem(row, 3, item_cant)

            # Columna 1, 2, y 5 no son editables
            for col in [0, 1, 2, 4, 5]:
                item_no_editable = QtWidgets.QTableWidgetItem()
                item_no_editable.setFlags(item_no_editable.flags() & ~QtCore.Qt.ItemIsEditable)
                self.tabla_productos.setItem(row, col, item_no_editable)

        self.imagen_cargos= QLabel(self)
        pixmap = QPixmap("AJUSTES.png")
        self.imagen_cargos.setPixmap(pixmap)
        self.imagen_cargos.setGeometry(QtCore.QRect(150, 10, 780, 55))
        self.imagen_cargos.show()

        # Crear la imagen clicable
        self.preliminar = ClickableLabel(self)  # Usar la clase ClickableLabel
        pixmap = QPixmap("preliminar.png")
        self.preliminar.setPixmap(pixmap)
        self.preliminar.setGeometry(QtCore.QRect(700, 605, 750, 55))
        self.preliminar.show()

        self.label_total_cantidad = QtWidgets.QLabel(MainWindow)
        self.label_total_cantidad.setGeometry(QtCore.QRect(775, 570, 300, 20))
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_total_cantidad.setFont(font)
        self.label_total_cantidad.setStyleSheet("QLabel {\n"
        "    color: black; /* Cambia el color del texto a rojo */\n"
        "}")

        self.label_total_item = QtWidgets.QLabel(MainWindow)
        self.label_total_item.setGeometry(QtCore.QRect(775, 588, 300, 20))
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_total_item.setFont(font)
        self.label_total_item.setStyleSheet("QLabel {\n"
        "    color: black; /* Cambia el color del texto a rojo */\n"
        "}")

        self.label_total = QtWidgets.QLabel(MainWindow)
        self.label_total.setGeometry(QtCore.QRect(775, 605, 350, 20))
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_total.setFont(font)
        self.label_total.setStyleSheet("QLabel {\n"
        "    color: black; /* Cambia el color del texto a rojo */\n"
        "}")

        self.tabla_visor_total = QtWidgets.QTableView(MainWindow)
        self.tabla_visor_total.setGeometry(QtCore.QRect(769, 539, 291, 115))



        self.campo_descripcion = QtWidgets.QLineEdit(MainWindow)
        self.campo_descripcion.setGeometry(QtCore.QRect(165, 130, 375, 26))
        self.campo_descripcion.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.campo_descripcion.setText("")

        self.label_referencial = QtWidgets.QLabel(MainWindow)
        self.label_referencial.setGeometry(QtCore.QRect(568, 135, 111, 16))
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(8)
        self.label_referencial.setFont(font)
        

        self.line_5 = QtWidgets.QFrame(MainWindow)
        self.line_5.setGeometry(QtCore.QRect(548, 77, 20, 101))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.campo_codigo_deposito = QtWidgets.QLineEdit(MainWindow)
        self.campo_codigo_deposito.setGeometry(QtCore.QRect(150, 87, 44, 26))
        self.campo_codigo_deposito.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.campo_codigo_deposito.setText("")
        self.campo_codigo_deposito.returnPressed.connect(self.abrir_ventana_depositos)

        self.label_autorizado = QtWidgets.QLabel(MainWindow)
        self.label_autorizado.setGeometry(QtCore.QRect(570, 93, 91, 16))
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(8)
        self.label_autorizado.setFont(font)


        self.line_4 = QtWidgets.QFrame(MainWindow)
        self.line_4.setGeometry(QtCore.QRect(71, 170, 980, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.campo_autorizado = QtWidgets.QLineEdit(MainWindow)
        self.campo_autorizado.setGeometry(QtCore.QRect(665, 88, 371, 26))
        self.campo_autorizado.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")

        self.label_descripcion = QtWidgets.QLabel(MainWindow)
        self.label_descripcion.setGeometry(QtCore.QRect(90, 133, 71, 21))
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(8)
        self.label_descripcion.setFont(font)

        self.campo_deposito = QtWidgets.QLineEdit(MainWindow)
        self.campo_deposito.setGeometry(QtCore.QRect(200, 87, 341, 26))
        self.campo_deposito.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.campo_deposito.setDisabled(True)

        self.line = QtWidgets.QFrame(MainWindow)
        self.line.setGeometry(QtCore.QRect(71, 70, 980, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line_3 = QtWidgets.QFrame(MainWindow)
        self.line_3.setGeometry(QtCore.QRect(1040, 77, 20, 101))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line_2 = QtWidgets.QFrame(MainWindow)
        self.line_2.setGeometry(QtCore.QRect(62, 77, 20, 101))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.campo_referencial = QtWidgets.QLineEdit(MainWindow)
        self.campo_referencial.setGeometry(QtCore.QRect(955, 130, 81, 26))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.campo_referencial.setFont(font)
        self.campo_referencial.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.campo_referencial.setStyleSheet("QLineEdit {\n"
        "                background-color: #1bb0b0; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #ffffff; /* Color del texto blanco */\n"
        "                font-weight: bold;\n"
        "            }")
        self.campo_referencial.setText("")
        self.campo_referencial.setAlignment(QtCore.Qt.AlignCenter)
        self.cargar_factor_referencial()

        self.label_deposito = QtWidgets.QLabel(MainWindow)
        self.label_deposito.setGeometry(QtCore.QRect(90, 90, 61, 21))
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(8)
        self.label_deposito.setFont(font)

        self.label_cargo = QtWidgets.QLabel(MainWindow)
        self.label_cargo.setGeometry(QtCore.QRect(775, 540, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_cargo.setFont(font)
        self.label_cargo.setStyleSheet("QLabel {\n"
        "    color: black; /* Cambia el color del texto a rojo */\n"
        "    font-size: 16px; /* Cambia el tamaño del texto a 20 píxeles */\n"
        "}")

        self.contadors_cargo = QtWidgets.QLabel(MainWindow)
        self.contadors_cargo.setGeometry(QtCore.QRect(850, 540, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.contadors_cargo.setFont(font)
        self.contadors_cargo.setStyleSheet("QLabel {\n"
        "    color: RED; /* Cambia el color del texto a rojo */\n"
        "    font-size: 16px; /* Cambia el tamaño del texto a 20 píxeles */\n"
        "}")
        self.contadors_cargo.setAlignment(QtCore.Qt.AlignRight)

        self.total_cantidad = QtWidgets.QLabel(MainWindow)
        self.total_cantidad.setGeometry(QtCore.QRect(685, 513, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.total_cantidad.setFont(font)
        self.total_cantidad.setStyleSheet("QLabel {\n"
        "    color: RED; /* Cambia el color del texto a rojo */\n"
        "    font-size: 16px; /* Cambia el tamaño del texto a 20 píxeles */\n"
        "}")
        self.total_cantidad.setAlignment(QtCore.Qt.AlignRight)

        self.label_total_referencial = QtWidgets.QLabel(MainWindow)
        self.label_total_referencial.setGeometry(QtCore.QRect(775, 635, 350, 20))
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_total_referencial.setFont(font)
        self.label_total_referencial.setStyleSheet("QLabel {\n"
        "    color: red; /* Cambia el color del texto */\n"
        "}")

        self.label_factor_referencial = QtWidgets.QLabel(MainWindow)
        self.label_factor_referencial.setGeometry(QtCore.QRect(695, 135, 240, 16))
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(8)
        self.label_factor_referencial.setFont(font)
        
        self.label_factor_referencial.setStyleSheet("QLabel {\n"
        "    color: blue; /* Cambia el color del texto */\n"
        "    font-size: 12px; /* Cambia el tamaño del texto a 20 píxeles */\n"
        "}")

        self.button_producto = QtWidgets.QPushButton(MainWindow)
        self.button_producto.setGeometry(QtCore.QRect(353, 620, 107, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        self.button_producto.setFont(font)
        self.button_producto.setStyleSheet("QPushButton {\n"
        "                background-color: #008080; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: 5px; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #00698f; /* Color cuando se presiona el botón */\n"
        "            }\n"
        "            QPushButton:disabled {\n"
        "                background-color: #ccc; /* Color cuando el botón está deshabilitado */\n"
        "            }")
        self.button_producto.clicked.connect(self.abrir_ventana_productos)
        self.shortcut_producto = QShortcut(QKeySequence("F1"), self)
        self.shortcut_producto.activated.connect(self.abrir_ventana_productos)

        self.button_totalizar = hoverButton(self)
        self.button_totalizar.setGeometry(QtCore.QRect(583, 620, 110, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        self.button_totalizar.setFont(font)
        self.button_totalizar.setStyleSheet("QPushButton {\n"
        "                background-color: #008080; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: 5px; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #ff0000; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #ab0000; /* Color cuando se presiona el botón */\n"
        "            }")
        self.button_totalizar.clicked.connect(self.confirmar_y_totalizar)
        self.shortcut_totalizar = QShortcut(QKeySequence("F3"), self)
        self.shortcut_totalizar.activated.connect(self.confirmar_y_totalizar)

        self.button_cancelar = QtWidgets.QPushButton(MainWindow)
        self.button_cancelar.setGeometry(QtCore.QRect(467, 620, 108, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        self.button_cancelar.setFont(font)
        self.button_cancelar.setStyleSheet("QPushButton {\n"
        "                background-color: #008080; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: 5px; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #00698f; /* Color cuando se presiona el botón */\n"
        "            }\n"
        "            QPushButton:disabled {\n"
        "                background-color: #ccc; /* Color cuando el botón está deshabilitado */\n"
        "            }")
        self.button_cancelar.clicked.connect(self.cancelar)
        self.shortcut_cancelar = QShortcut(QKeySequence("F2"), self)
        self.shortcut_cancelar.activated.connect(self.cancelar)

        self.tabla_visor_total.raise_()
        self.tabla_productos.raise_()
        self.label_total_cantidad.raise_()
        self.label_total_item.raise_()
        self.label_total.raise_()
        self.campo_descripcion.raise_()
        self.label_referencial.raise_()
        self.line_5.raise_()
        self.campo_codigo_deposito.raise_()
        self.label_autorizado.raise_()
        self.line_4.raise_()
        self.campo_autorizado.raise_()
        self.label_descripcion.raise_()
        self.campo_deposito.raise_()
        self.line.raise_()
        self.line_3.raise_()
        self.line_2.raise_()
        self.campo_referencial.raise_()
        self.label_deposito.raise_()
        self.label_cargo.raise_()
        self.contadors_cargo.raise_()
        self.total_cantidad.raise_()
        self.label_total_referencial.raise_()
        self.label_factor_referencial.raise_()
        self.button_producto.raise_()
        self.button_totalizar.raise_()
        self.button_cancelar.raise_()

        self.campo_referencial.setDisabled(True)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Form", "ZISCON ADMINISTRATIVO (V 1.0)"))
        MainWindow.setWindowIcon(QIcon('icono.png'))
        item = self.tabla_productos.horizontalHeaderItem(0)
        item.setText(_translate("Form", "CODIGO"))
        item = self.tabla_productos.horizontalHeaderItem(1)
        item.setText(_translate("Form", "DESCRIPCION"))
        item = self.tabla_productos.horizontalHeaderItem(2)
        item.setText(_translate("Form", "UND."))
        item = self.tabla_productos.horizontalHeaderItem(3)
        item.setText(_translate("Form", "CONTEO"))
        item = self.tabla_productos.horizontalHeaderItem(4)
        item.setText(_translate("Form", "EXISTENCIA"))
        item = self.tabla_productos.horizontalHeaderItem(5)
        item.setText(_translate("Form", "DIFERENCIA"))
        self.label_total_cantidad.setText(_translate("Form", "TOTAL CANTIDAD:"))
        self.label_total_item.setText(_translate("Form", "TOTAL ITEM:"))
        self.label_total.setText(_translate("Form", "TOTAL:"))
        self.label_referencial.setText(_translate("Form", "Factor Referencial :"))
        self.label_autorizado.setText(_translate("Form", "Autorizado por:"))
        self.label_descripcion.setText(_translate("Form", "Descripción:"))
        self.label_deposito.setText(_translate("Form", "Deposito:"))
        self.label_cargo.setText(_translate("Form", "CARGO N°"))
        self.contadors_cargo.setText(_translate("Form", ""))
        self.total_cantidad.setText(_translate("Form", ""))
        self.label_total_referencial.setText(_translate("Form", "REFERENCIAL:"))
        self.label_factor_referencial.setText(_translate("Form", "***BANCO CENTRAL DE VENEZUELA***"))
        self.button_producto.setText(_translate("Form", "PRODUCTO [F1]"))
        self.button_totalizar.setText(_translate("Form", "TOTALIZAR [F3]"))
        self.button_cancelar.setText(_translate("Form", "CANCELAR [F2]"))

    def actualizar_fila_actual(self, row, column):
        if column == 0:  # Solo si se editó la columna 0 (código)
            self.fila_actual = row  # Actualiza la fila actual
            print(f"Fila actual actualizada a: {self.fila_actual}")

    def on_item_selected(self, item):
        self.fila_actual = item.row()  # Actualiza la fila actual al seleccionar un item

    def cargar_deposito_predeterminado(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nombre FROM depositos WHERE codigo = '01'")
        deposito = cursor.fetchone()
        conn.close()
        if deposito:
            self.campo_codigo_deposito.setText(deposito[0])
            self.campo_deposito.setText(deposito[1])

    def moverCursor(self, item):
        if item.column() == 3:  # Solo si se editó la columna 3
            self.tabla_productos.setCurrentCell(item.row(), 4)  # Mover el cursor a la siguiente celda

    def seleccionarFila(self):
        seleccion = self.tabla_productos.selectedItems()
        if seleccion:
            fila = seleccion[0].row()
            self.tabla_productos.selectRow(fila)
        else:
            self.tabla_productos.clearSelection()

    def abrir_ventana_productos(self):
        self.ventana = InventoryWindowAjuste(ventana_cargar=self, fila_actual=self.fila_actual)  # Pasa la ventana CargarProductos como parámetro
        self.ventana.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ventana.show()

    def abrir_ventana_depositos(self):
        # Crear una instancia de la ventana ya creada
        self.ventana_depositos = VentanaDepositos()

        # Conectar la señal deposito_seleccionado al método actualizar_campos_deposito
        self.ventana_depositos.deposito_seleccionado.connect(self.actualizar_campos_deposito)

        self.ventana_depositos.show()  # Mostrar la ventana

    def actualizar_campos_deposito(self, codigo, nombre):
        # Actualizar los campos con el código y nombre del depósito
        self.campo_codigo_deposito.setText(codigo)
        self.campo_deposito.setText(nombre)

    def itemChanged(self, item):           
        if item.column() == 3:  # Solo si se cambió el valor de la columna 3
            if item.text() != '':  # Verifica si la celda tiene un valor
                for col in [0, 1, 2, 4, 5]:
                    cell_item = self.tabla_productos.item(item.row(), col)
                    if cell_item:
                        cell_item.setFlags(cell_item.flags() & ~QtCore.Qt.ItemIsEditable)
                        
                conteo = float(item.text())  # Valor de la columna 3 (conteo)
            
                # Obtener el valor de la columna 4 (existencia)
                existencia_item = self.tabla_productos.item(item.row(), 4)  # Columna 4
                if existencia_item and existencia_item.text() != '':
                    existencia = float(existencia_item.text())  # Convertir a float
                else:
                    existencia = 0.0  # Si no hay existencia, establecer a 0

                # Calcular el resultado
                resultado = round(conteo - existencia, 2)

                # Mostrar el resultado en la columna 5
                self.tabla_productos.setItem(item.row(), 5, QtWidgets.QTableWidgetItem("{:,.2f}".format(resultado)))

            self.actualizar_total_cantidad()
            self.actualizar_total_item()
            self.actualizar_total()
            self.actualizar_total_referencial()
    
    def actualizar_total_cantidad(self):
        total_cantidad = 0
        for row in range(self.tabla_productos.rowCount()):
            item = self.tabla_productos.item(row, 3)  # Obtener el item de la columna 3
            if item is not None:  # Verificar que el item no sea None
                cantidad_text = item.text()  # Obtener el texto del item
                if cantidad_text != '':  # Verifica si la celda tiene un valor
                    total_cantidad += float(cantidad_text)
        self.label_total_cantidad.setText(f"TOTAL CANTIDAD:                          {total_cantidad:>5.0f}")

    def actualizar_total_item(self):
        total_item = self.calcular_total_item()
        self.label_total_item.setText(f"TOTAL ITEM:                                     {total_item:>5}")

    def actualizar_total(self):
        total = self.calcular_total()
        self.label_total.setText(f"TOTAL:                             Bs.{total:>15,.2f}")

    def actualizar_total_referencial(self):
        total = self.calcular_total_referencial()
        self.label_total_referencial.setText(f"REFERENCIAL:                   ${total:>15,.2f}")

    def calcular_total_cantidad(self):
        total_cantidad = 0
        for row in range(self.tabla.rowCount()):
            cantidad = self.tabla.item(row, 3).text()
            total_cantidad += int(cantidad)
        return total_cantidad

    def calcular_total(self):
        total = 0
        for row in range(self.tabla_productos.rowCount()):
            widget = self.tabla_productos.cellWidget(row, 5)
            if widget:
                layout = widget.layout()
                label1 = layout.itemAt(0).widget()
                total += float(label1.text().replace(',', ''))
        return total

    def calcular_total_referencial(self):
        total = 0
        for row in range(self.tabla_productos.rowCount()):
            # Obtener el costo de la columna 2
            costo_item = self.tabla_productos.item(row, 2)  # Suponiendo que el costo está en la columna 2
            if costo_item:
                costo = costo_item.data(QtCore.Qt.UserRole)  # Obtener el costo almacenado
                if costo is None:  # Verificar si el costo es None
                    print(f"Advertencia: El costo en la fila {row} es None.")
                    continue  # Saltar a la siguiente fila si el costo es None

                # Obtener la diferencia de la columna 5
                diferencia_item = self.tabla_productos.item(row, 5)  # Suponiendo que la diferencia está en la columna 5
                if diferencia_item:
                    diferencia_texto = diferencia_item.text().replace(',', '')  # Eliminar comas si es necesario
                    try:
                        diferencia = float(diferencia_texto) if diferencia_texto else 0  # Convertir a float
                    except ValueError:
                        print(f"Advertencia: La diferencia en la fila {row} no es un número válido.")
                        continue  # Saltar a la siguiente fila si la diferencia no es válida

                    # Calcular el total acumulado
                    total += costo * diferencia  # Multiplica el costo por la diferencia
                else:
                    print(f"Advertencia: No se encontró la diferencia en la fila {row}.")
        
        return total

    def calcular_total_item(self):
        total_item = 0
        for row in range(self.tabla_productos.rowCount()):
            item = self.tabla_productos.item(row, 0)  # Asumiendo que la columna 0 es el código del item
            if item is not None and item.text() != '':  # Verifica si la celda tiene un valor
                total_item += 1
        return total_item

    def cargar_contador_cargos(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ajuste_inventario FROM correlativos WHERE ajuste_inventario IS NOT NULL ORDER BY id DESC LIMIT 1;')
        result = cursor.fetchone()
        if result:
            self.contador_cargos = int(result[0])
        else:
            self.contador_cargos = 1  # Valor por defecto si no se encuentra
        conn.close()

    def actualizar_contador_cargos(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        
        # Actualizar el contador en la tabla correlativos
        cursor.execute('''
            INSERT INTO correlativos (ajuste_inventario) VALUES (?)
            ON CONFLICT(id) DO UPDATE SET ajuste_inventario = excluded.ajuste_inventario;
        ''', (self.contador_cargos,))
        
        conn.commit()
        conn.close()

    def confirmar_y_totalizar(self):
        # Verificar si hay productos cargados en la tabla
        hay_productos = False
        for row in range(self.tabla_productos.rowCount()):
            codigo = self.tabla_productos.item(row, 0)  # Suponiendo que la columna 0 es el código del producto
            if (codigo is not None and codigo.text().strip() != ""):
                hay_productos = True
                break

        if not hay_productos:
            QMessageBox.warning(self, "Error", "No hay productos cargados en la tabla. No se puede totalizar.")
            return

        # Mostrar un cuadro de diálogo de confirmación
        respuesta = QMessageBox.question(self, "Confirmación", "¿Está seguro de totalizar?", QMessageBox.Yes | QMessageBox.No)

        if respuesta == QMessageBox.Yes:
            self.totalizar()  # Llamar a la función totalizar si el usuario confirma

    def totalizar(self):
        # Obtener el contador de cargos
        contador_cargos = self.contador_cargos

        # Obtener el depósito seleccionado
        deposito_seleccionado = self.campo_deposito.text()

        # Obtener el ID del depósito seleccionado
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM depositos WHERE nombre = ?", (deposito_seleccionado,))
        deposito_id = cursor.fetchone()
        
        if deposito_id is None:
            QMessageBox.warning(self, "Error", "Depósito no encontrado.")
            return

        deposito_id = deposito_id[0]

        # Generar el "cargo_numero" basado en el contador de cargos
        cargo_numero = f"{contador_cargos:08d}"

        # Recorrer la tabla de productos para obtener los datos
        for row in range(self.tabla_productos.rowCount()):
            codigo_producto = self.tabla_productos.item(row, 0).text()  # Código del producto
            conteo = self.tabla_productos.item(row, 3).text()  # Conteo

            if codigo_producto and conteo:  # Verificar que el código y la cantidad no estén vacíos
                conteo = int(conteo)  # Convertir a entero

                # Verificar si el producto ya existe en la tabla existencia_productos
                cursor.execute("SELECT cantidad FROM existencia_productos WHERE codigo = ? AND deposito = ?", (codigo_producto, deposito_id))
                resultado = cursor.fetchone()

                if resultado:  # Si el producto ya existe, actualizar la cantidad
                    cursor.execute('''UPDATE existencia_productos
                        SET cantidad = ?, cargo_numero = ?, fecha_registro = ?, autorizado = ?
                        WHERE codigo = ? AND deposito = ?''', (conteo, cargo_numero, datetime.now().strftime("%Y-%m-%d"), self.campo_autorizado.text(), codigo_producto, deposito_id))
                else:  # Si no existe, insertar un nuevo registro
                    cursor.execute('''INSERT INTO existencia_productos (codigo, deposito, cantidad, cargo_numero, fecha_registro, autorizado)
                        VALUES (?, ?, ?, ?, ?, ?)''', (codigo_producto, deposito_id, conteo, cargo_numero, datetime.now().strftime("%Y-%m-%d"), self.campo_autorizado.text()))

        # Confirmar los cambios
        conn.commit()
        conn.close()

        # Generar y guardar el PDF
        pdf_filename = self.generar_pdf(cargo_numero)

        # Verificar si el archivo se ha creado
        if os.path.exists(pdf_filename):
            os.startfile(pdf_filename)  # Abrir el archivo PDF en el visor predeterminado
        else:
            print(f"Error: El archivo {pdf_filename} no se encontró.")

        # Registrar la carga en el historial
        self.registrar_carga(cargo_numero, self.campo_autorizado.text())

        # Al final de la operación, incrementa el contador de cargos
        self.contador_cargos += 1  # Incrementa el contador
        self.contadors_cargo.setText(f"{self.contador_cargos:08d}")  # Actualiza la etiqueta con el nuevo número de cargo

        # Actualizar el contador en la base de datos
        self.actualizar_contador_cargos()

        # Limpiar la ventana para una nueva carga
        self.limpiar_ventana()

    def limpiar_ventana(self):
        # Limpiar los campos de texto
        self.campo_descripcion.clear()
        self.campo_autorizado.clear()

        # Limpiar la tabla de productos
        self.tabla_productos.setRowCount(0)  # Elimina todas las filas de la tabla
        self.tabla_productos.setRowCount(50)  # Restablece el número de filas si es necesario

        # Asegurarse de que las celdas sean editables
        for row in range(self.tabla_productos.rowCount()):
            for col in [0, 3]:  # Columnas editables (código y cantidad)
                item = QTableWidgetItem()
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                self.tabla_productos.setItem(row, col, item)

        # Limpiar etiquetas de totales
        self.label_total_cantidad.setText("TOTAL CANTIDAD:")
        self.label_total_item.setText("TOTAL ITEM:")
        self.label_total.setText("TOTAL:")
        self.label_total_referencial.setText("REFERENCIAL:")

        # Restablecer el contador de cargos en la interfaz
        self.contadors_cargo.setText(f"{self.contador_cargos:08d}")  # Asegúrate de que el contador se muestre correctamente

    def generar_pdf(self, cargo_numero):
        # Obtener la ruta del directorio donde se encuentra el script
        directorio_script = os.path.dirname(os.path.abspath(__file__))

        # crear carpeta si no existe
        carpeta_destino = os.path.join(directorio_script, "Cargos_inventario")

        os.makedirs(carpeta_destino, exist_ok=True)  # Crear la carpeta si no existe

        # Crear el archivo PDF
        pdf_filename = os.path.join(carpeta_destino, f"cargo_inventario_{cargo_numero}.pdf")  # Ruta completa
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter, topMargin=10, bottomMargin=1)
        styles = getSampleStyleSheet()
        story = []

        # Conectar a la base de datos y obtener la información de la empresa
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT razon_social, rif, direccion, whatsapp, correo, logo_path FROM informacion_empresa LIMIT 1")
        empresa_info = cursor.fetchone()
        conn.close()

        # Verificar si se obtuvo información
        if empresa_info:
            razon_social, rif, direccion, whatsapp, correo, logo_path = empresa_info
        else:
            razon_social = rif = direccion = whatsapp = correo = logo_path = "Información no disponible"

        # Crear un logo Image
        if logo_path:
            logo_image = Image(logo_path)
            view_width = 190  # Ajusta el ancho según sea necesario
            view_height = 60  # Ajusta la altura según sea necesario

            # Escalar el logo al tamaño deseado
            logo_image.drawWidth = view_width
            logo_image.drawHeight = view_height
        else:
            logo_image = None  # Si no hay logo, puedes manejarlo como desees

        # Definir un marco para el contenido
        frame = Frame(doc.leftMargin, doc.bottomMargin + 50, doc.width, doc.height - 50, id='normal')

        # Crear una plantilla de página que incluya el número de página
        template = PageTemplate(id='my_template', frames=[frame], onPage=self.add_page_number)
        doc.addPageTemplates([template])

        # Crear una tabla para la información de la empresa y el logo
        data = [
            [
                Paragraph(
                    f"<b>Razón Social:</b> {razon_social}<br/>"
                    f"<b>RIF:</b> {rif}<br/>"
                    f"<b>Dirección:</b> {direccion}<br/>"
                    f"<b>Whatsapp:</b> {whatsapp}<br/>"
                    f"<b>Correo:</b> {correo}",
                    styles['Normal']
                ),
                logo_image
            ]
        ]

        # Crear la tabla
        table = Table(data, colWidths=[330, 135])  # Ajusta los anchos según sea necesario
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica', 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente al centro
        ]))

        story.append(table)
        story.append(Spacer(1, 2))

        # Agregar una línea como un Drawing
        line = Drawing(doc.width, 0.5)  # Ancho del documento y altura de la línea
        line.add(Line(-50, 0, 510, 0))  # Línea horizontal
        line.contents[0].strokeColor = colors.black  # Establecer el color de la línea

        # Agregar la línea al story
        story.append(line)

        # Agregar un Spacer para crear espacio entre la tabla de productos y la tabla de totales
        story.append(Spacer(1, 2))  # Espacio de 12 unidades

        # Título del PDF
        titulo = Paragraph("Ajustes de Inventario", styles['Title'])
        story.append(titulo)
        story.append(Spacer(1, 6))

        styles['Normal'].leftIndent = -50

        # Crear una tabla para el factor y la fecha/hora
        data_info = [
        [f"Depósito: {self.campo_codigo_deposito.text()} - {self.campo_deposito.text()} ", f"Número de Ajuste: {self.contadors_cargo.text()}"]
        ]

        # Crear la tabla
        info_table = Table(data_info, colWidths=[410, 160]) # Ajusta los anchos según sea necesario
        info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (-1, 0), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        # Agregar la tabla a la historia
        story.append(info_table)
        story.append(Spacer(1, 6))


        # Crear datos para la tabla
        data_info = [
        ["Descripción:", self.campo_descripcion.text()],
        ["Autorizado por:", self.campo_autorizado.text()]
        ]

        # Crear la tabla
        info_table = Table(data_info, colWidths=[100, 470]) # Ajusta los anchos según sea necesario
        info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0, colors.white), # Sin líneas internas
        ]))

        # Agregar la tabla a la historia
        story.append(info_table)
        story.append(Spacer(1, 6)) # Espacio de 20 unidades


        # Obtener la fecha y hora actuales
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")

        # Crear una tabla para el factor y la fecha/hora
        data_info = [
        [f"Factor Referencial: {self.campo_referencial.text()}", f"FECHA: {fecha_actual} | HORA: {hora_actual}"]
        ]

        # Crear la tabla
        info_table = Table(data_info, colWidths=[370, 200]) # Ajusta los anchos según sea necesario
        info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        # Agregar la tabla a la historia
        story.append(info_table)
        story.append(Spacer(1, 6))

       # Datos de la tabla de productos (solo filas con datos)
        data = [["Código", "Descripción", "Cantidad", "Existencia", "Diferencia"]]
        for row in range(self.tabla_productos.rowCount()):
            codigo = self.tabla_productos.item(row, 0) # Verificar si la celda de la columna 0 tiene datos
            if codigo and codigo.text().strip(): # Si la celda no está vacía
                descripcion = self.tabla_productos.item(row, 1).text() if self.tabla_productos.item(row, 1) else ""
                cantidad = self.tabla_productos.item(row, 3).text() if self.tabla_productos.item(row, 3) else ""
                existencia = self.tabla_productos.item(row, 4).text() if self.tabla_productos.item(row, 4) else ""
                diferencia = self.tabla_productos.item(row, 5).text() if self.tabla_productos.item(row, 5) else ""
                        
                data.append([codigo.text(), descripcion, cantidad, existencia, diferencia])

        # Crear la tabla
        tabla = Table(data, colWidths=[80, 300, 50, 50, 80, 80])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ]))
        story.append(tabla)

        # Calcular la altura de la tabla
        table_height = tabla.wrap(doc.width, doc.height)[1]

        # Verificar si hay suficiente espacio en la página
        if table_height < doc.height - 100:  # Ajusta el valor según sea necesario

            # Agregar un Spacer para crear espacio entre la tabla de productos y la tabla de totales
            story.append(Spacer(1, 12))  # Espacio de 12 unidades

            # Totales
            total_item = self.label_total_item.text().split(":")[-1].strip()
            total_cantidad = self.label_total_cantidad.text().split(":")[-1].strip()
            total_referencial = self.label_total_referencial.text().split(":")[-1].strip()

            # Crear datos para la tabla de totales
            totales_data = [
                [f"Total Ítem: {total_item}", "Total Referencial:", total_referencial],
                [f"Total Cantidad: {total_cantidad}"],
            ]

            # Crear la tabla de totales
            tabla_totales = Table(totales_data, colWidths=[390, 80])
            tabla_totales.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Borde externo
            ]))

            # Agregar la tabla de totales a la historia
            story.append(Spacer(1, 5))
            story.append(tabla_totales)

        try:
            doc.build(story)
        except Exception as e:
            print(f"Error al generar el PDF: {e}")

        return pdf_filename

    def registrar_carga(self, numero_cargo, autorizado):
        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Insertar un nuevo registro en la tabla historial_cargas
        cursor.execute('''
            INSERT INTO historial_ajustes (numero_cargo, autorizado)
            VALUES (?, ?)
        ''', (numero_cargo, autorizado))

        # Confirmar los cambios
        conn.commit()
        conn.close()

    def cargar_factor_referencial(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Obtener el factor de inventario de la moneda dólares
        cursor.execute("SELECT factor_inventario FROM monedas WHERE nombre = 'Dolares'")
        factor_inventario_dolares = cursor.fetchone()[0]

        # Asignar el valor a la variable moneda_referencial_edit
        self.campo_referencial.setText(str(factor_inventario_dolares))

        conn.close()

    def preliminar_operacion(self):
        # Crear un objeto BytesIO para el PDF en memoria
        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=10, bottomMargin=1)
        styles = getSampleStyleSheet()
        story = []

        # Conectar a la base de datos y obtener la información de la empresa
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT razon_social, rif, direccion, whatsapp, correo, logo_path FROM informacion_empresa LIMIT 1")
        empresa_info = cursor.fetchone()
        conn.close()

        # Verificar si se obtuvo información
        if empresa_info:
            razon_social, rif, direccion, whatsapp, correo, logo_path = empresa_info
        else:
            razon_social = rif = direccion = whatsapp = correo = logo_path = "Información no disponible"

        # Crear un logo Image
        if logo_path:
            logo_image = Image(logo_path)
            view_width = 190  # Ajusta el ancho según sea necesario
            view_height = 60  # Ajusta la altura según sea necesario

            # Escalar el logo al tamaño deseado
            logo_image.drawWidth = view_width
            logo_image.drawHeight = view_height
        else:
            logo_image = None  # Si no hay logo, puedes manejarlo como desees

        # Definir un marco para el contenido
        frame = Frame(doc.leftMargin, doc.bottomMargin + 50, doc.width, doc.height - 50, id='normal')

        # Crear una plantilla de página que incluya el número de página
        template = PageTemplate(id='my_template', frames=[frame], onPage=self.add_page_number)
        doc.addPageTemplates([template])

        # Crear una tabla para la información de la empresa y el logo
        data = [
            [
                Paragraph(
                    f"<b>Razón Social:</b> {razon_social}<br/>"
                    f"<b>RIF:</b> {rif}<br/>"
                    f"<b>Dirección:</b> {direccion}<br/>"
                    f"<b>Whatsapp:</b> {whatsapp}<br/>"
                    f"<b>Correo:</b> {correo}",
                    styles['Normal']
                ),
                logo_image
            ]
        ]

        # Crear la tabla
        table = Table(data, colWidths=[330, 135])  # Ajusta los anchos según sea necesario
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica', 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente al centro
        ]))

        story.append(table)

        # Agregar una línea como un Drawing
        line = Drawing(doc.width, 0.5)  # Ancho del documento y altura de la línea
        line.add(Line(-50, 0, 510, 0))  # Línea horizontal
        line.contents[0].strokeColor = colors.black  # Establecer el color de la línea

        # Agregar la línea al story
        story.append(line)

        # Agregar un Spacer para crear espacio entre la tabla de productos y la tabla de totales
        story.append(Spacer(1, 2))  # Espacio de 12 unidades

        # Título del PDF
        titulo = Paragraph("Ajustes de Inventario", styles['Title'])
        story.append(titulo)
        story.append(Spacer(1, 6))

        styles['Normal'].leftIndent = -50

        # Crear una tabla para el factor y la fecha/hora
        data_info = [
        [f"Depósito: {self.campo_codigo_deposito.text()} - {self.campo_deposito.text()} ", f"Número de Ajuste: {self.contadors_cargo.text()}"]
        ]

        # Crear la tabla
        info_table = Table(data_info, colWidths=[410, 160]) # Ajusta los anchos según sea necesario
        info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (-1, 0), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        # Agregar la tabla a la historia
        story.append(info_table)
        story.append(Spacer(1, 6))


        # Crear datos para la tabla
        data_info = [
        ["Descripción:", self.campo_descripcion.text()],
        ["Autorizado por:", self.campo_autorizado.text()]
        ]

        # Crear la tabla
        info_table = Table(data_info, colWidths=[100, 470]) # Ajusta los anchos según sea necesario
        info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0, colors.white), # Sin líneas internas
        ]))

        # Agregar la tabla a la historia
        story.append(info_table)
        story.append(Spacer(1, 6)) # Espacio de 20 unidades


        # Obtener la fecha y hora actuales
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        hora_actual = datetime.now().strftime("%H:%M:%S")

        # Crear una tabla para el factor y la fecha/hora
        data_info = [
        [f"Factor Referencial: {self.campo_referencial.text()}", f"FECHA: {fecha_actual} | HORA: {hora_actual}"]
        ]

        # Crear la tabla
        info_table = Table(data_info, colWidths=[370, 200]) # Ajusta los anchos según sea necesario
        info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        # Agregar la tabla a la historia
        story.append(info_table)
        story.append(Spacer(1, 6))

        # Datos de la tabla de productos (solo filas con datos)
        data = [["Código", "Descripción", "Cantidad", "Existencia", "Diferencia"]]
        for row in range(self.tabla_productos.rowCount()):
            codigo = self.tabla_productos.item(row, 0) # Verificar si la celda de la columna 0 tiene datos
            if codigo and codigo.text().strip(): # Si la celda no está vacía
                descripcion = self.tabla_productos.item(row, 1).text() if self.tabla_productos.item(row, 1) else ""
                cantidad = self.tabla_productos.item(row, 3).text() if self.tabla_productos.item(row, 3) else ""
                existencia = self.tabla_productos.item(row, 4).text() if self.tabla_productos.item(row, 4) else ""
                diferencia = self.tabla_productos.item(row, 5).text() if self.tabla_productos.item(row, 5) else ""
                        
                data.append([codigo.text(), descripcion, cantidad, existencia, diferencia])

        # Crear la tabla
        tabla = Table(data, colWidths=[80, 300, 50, 50, 80, 80])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ]))
        story.append(tabla)

        # Calcular la altura de la tabla
        table_height = tabla.wrap(doc.width, doc.height)[1]

        # Verificar si hay suficiente espacio en la página
        if table_height < doc.height - 100:  # Ajusta el valor según sea necesario

            # Agregar un Spacer para crear espacio entre la tabla de productos y la tabla de totales
            story.append(Spacer(1, 12))  # Espacio de 12 unidades

            # Totales
            total_item = self.label_total_item.text().split(":")[-1].strip()
            total_cantidad = self.label_total_cantidad.text().split(":")[-1].strip()
            total_referencial = self.label_total_referencial.text().split(":")[-1].strip()

            # Crear datos para la tabla de totales
            totales_data = [
                [f"Total Ítem: {total_item}", "Total Referencial:", total_referencial],
                [f"Total Cantidad: {total_cantidad}"],
            ]

            # Crear la tabla de totales
            tabla_totales = Table(totales_data, colWidths=[390, 80])
            tabla_totales.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Borde externo
            ]))

            # Agregar la tabla de totales a la historia
            story.append(Spacer(1, 5))
            story.append(tabla_totales)

        # Generar el PDF
        doc.build(story)

        # Mover el puntero al inicio del buffer
        pdf_buffer.seek(0)

        # Abrir la ventana del PDF
        self.ventana_pdf = VentanaPDF(pdf_buffer)
        self.ventana_pdf.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ventana_pdf.show()

    def add_page_number(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Oblique", 10)
        canvas.setFillColorRGB(0.27, 0.27, 0.27)
        canvas.drawString(290, 10, f"Page {doc.page}")
        canvas.restoreState()

    def cancelar(self):
        # Limpiar la ventana para una nueva carga
        self.limpiar_ventana()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:  # Si se presiona la tecla Delete
            fila = self.tabla_productos.currentRow()
            if fila != -1:
                producto = self.tabla_productos.item(fila, 0)
                if producto is not None and producto.text() != "":
                    mensaje = QMessageBox.question(self, "Eliminar item", "¿Está seguro de eliminar el item?")
                    if mensaje == QMessageBox.Yes:
                        self.tabla_productos.removeRow(fila)
                        self.actualizar_total_cantidad()  # Actualiza el total de cantidad
                        self.actualizar_total_item()      # Actualiza el total de items
                        self.actualizar_total()            # Actualiza el total
                        self.actualizar_total_referencial() # Actualiza el total referencial
                    else:
                        # No hacer nada si la fila está vacía
                        pass

        if event.key() == QtCore.Qt.Key_Return:  # Verificar si se presionó la tecla Enter
            current_row = self.tabla_productos.currentRow()
            current_column = self.tabla_productos.currentColumn()
            if current_column == 3:
                self.tabla_productos.setCurrentCell(current_row, 4)  # Mover el cursor a la siguiente celda
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = AjusteProductos()
    MainWindow.show()
    sys.exit(app.exec_())