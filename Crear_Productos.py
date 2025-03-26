import sys
import json
import barcode
import pandas as pd
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QListView, QGraphicsView, QGraphicsScene, QFileDialog, QAbstractItemView, QGraphicsPixmapItem, QTableWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel, QIntValidator, QValidator, QDoubleValidator, QRegExpValidator, QPixmap
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QTableWidgetItem, QLabel
from PyQt5.QtCore import QTimer,QDateTime, Qt, QRegExp
from Crear_Marcas import ConfiguracionMarcas
from Linea_Inventario import ConfiguracionLinea
import time
import os
import subprocess
import re
import asteval
import sqlite3

class MathValidator(QValidator):
    def __init__(self):
        super(MathValidator, self).__init__()

    def validate(self, input_str, pos):
        # Permitir solo números, operadores y paréntesis
        pattern = r'^[0-9+\-*/()$. ]+$'
        if re.match(pattern, input_str):
            return (QValidator.Acceptable, input_str, pos)
        elif re.match(r'^[0-9+\-*/()$. ]*$', input_str):
            return (QValidator.Intermediate, input_str, pos)
        else:
            return (QValidator.Invalid, input_str, pos)

    def fixup(self, input_str):
        # No hacer nada en este caso
        pass

class SeleccionImpuestos(QtWidgets.QDialog):  # Hereda de QWidget
    def __init__(self, impuestos_predeterminados=None, es_nuevo_producto=True):
        super().__init__()  # Llama al constructor de QWidget
        self.impuestos = self.obtener_impuestos_activos()
        self.impuestos_predeterminados = impuestos_predeterminados or {}
        self.es_nuevo_producto = es_nuevo_producto  # Nuevo parámetro
        self.setupUi()
        self.actualizar_checkboxes()

    def obtener_impuestos_activos(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        
        # Ajusta la consulta según tu esquema. Suponiendo que hay una columna 'activo' que indica si el impuesto está activo.
        cursor.execute("SELECT nombre, activo FROM impuestos WHERE activo = 1")  # Solo selecciona impuestos activos
        resultados = cursor.fetchall()
        
        conn.close()
        
        # Convertir los resultados a una lista de diccionarios
        impuestos = []
        for nombre, activo in resultados:
            impuestos.append({"nombre": nombre, "activo": bool(activo)})  # Asegúrate de que 'activo' sea un booleano
        
        return impuestos

    def setupUi(self):
        self.setObjectName("Seleccion_impuestos")
        self.resize(229, 300)
        self.fondo = QtWidgets.QListView(self)
        self.fondo.setGeometry(QtCore.QRect(1, 1, 226, 298))
        self.fondo.setStyleSheet("background-color: rgb(244, 255, 255);")
        self.fondo.setObjectName("fondo")

        self.fondo_1 = QtWidgets.QListView(self)
        self.fondo_1.setGeometry(QtCore.QRect(3, 30, 221, 231))
        self.fondo_1.setObjectName("fondo_1")

        self.iva_check = QtWidgets.QCheckBox(self)
        self.iva_check.setGeometry(QtCore.QRect(7, 33, 100, 31))
        self.iva_check.setStyleSheet("""
            QCheckBox {  
                border: none; 
                border-radius: 5px; 
                padding: 5px;
                color: #000000 
            }
            QCheckBox::indicator {
                width: 20px; /* Ancho del indicador */
                height: 20px; /* Alto del indicador */
                border: 1px solid #ccc; /* Borde del indicador */
                border-radius: 5px; /* Radio del borde del indicador */
                background-color: #fff; /* Color de fondo del indicador */
            }
            QCheckBox::indicator:checked {
                background-color: #1bb0b0; /* Color de fondo del indicador cuando se selecciona */
            }
        """)
        self.iva_check.setObjectName("iva_check")

        self.iva_percibido_check = QtWidgets.QCheckBox(self)
        self.iva_percibido_check.setGeometry(QtCore.QRect(7, 57, 115, 31))
        self.iva_percibido_check.setStyleSheet("""
            QCheckBox {  
                border: none; 
                border-radius: 5px; 
                padding: 5px;
                color: #000000 
            }
            QCheckBox::indicator {
                width: 20px; /* Ancho del indicador */
                height: 20px; /* Alto del indicador */
                border: 1px solid #ccc; /* Borde del indicador */
                border-radius: 5px; /* Radio del borde del indicador */
                background-color: #fff; /* Color de fondo del indicador */
            }
            QCheckBox::indicator:checked {
                background-color: #1bb0b0; /* Color de fondo del indicador cuando se selecciona */
            }
        """)
        self.iva_percibido_check.setObjectName("iva_percibido_check")

        self.ial_check = QtWidgets.QCheckBox(self)
        self.ial_check.setGeometry(QtCore.QRect(7, 80, 101, 31))
        self.ial_check.setStyleSheet("""
            QCheckBox {  
                border: none; 
                border-radius: 5px; 
                padding: 5px;
                color: #000000 
            }
            QCheckBox::indicator {
                width: 20px; /* Ancho del indicador */
                height: 20px; /* Alto del indicador */
                border: 1px solid #ccc; /* Borde del indicador */
                border-radius: 5px; /* Radio del borde del indicador */
                background-color: #fff; /* Color de fondo del indicador */
            }
            QCheckBox::indicator:checked {
                background-color: #1bb0b0; /* Color de fondo del indicador cuando se selecciona */
            }
        """)
        self.ial_check.setObjectName("ial_check")

        self.igtf_check = QtWidgets.QCheckBox(self)
        self.igtf_check.setGeometry(QtCore.QRect(7, 103, 101, 31))
        self.igtf_check.setStyleSheet("""
            QCheckBox {  
                border: none; 
                border-radius: 5px; 
                padding: 5px;
                color: #000000 
            }
            QCheckBox::indicator {
                width: 20px; /* Ancho del indicador */
                height: 20px; /* Alto del indicador */
                border: 1px solid #ccc; /* Borde del indicador */
                border-radius: 5px; /* Radio del borde del indicador */
                background-color: #fff; /* Color de fondo del indicador */
            }
            QCheckBox::indicator:checked {
                background-color: #1bb0b0; /* Color de fondo del indicador cuando se selecciona */
            }
        """)
        self.igtf_check.setObjectName("igtf_check")

        self.exento_check = QtWidgets.QCheckBox(self)
        self.exento_check.setGeometry(QtCore.QRect(7, 127, 101, 31))
        self.exento_check.setStyleSheet("""
            QCheckBox {  
                border: none; 
                border-radius: 5px; 
                padding: 5px;
                color: #000000 
            }
            QCheckBox::indicator {
                width: 20px; /* Ancho del indicador */
                height: 20px; /* Alto del indicador */
                border: 1px solid #ccc; /* Borde del indicador */
                border-radius: 5px; /* Radio del borde del indicador */
                background-color: #fff; /* Color de fondo del indicador */
            }
            QCheckBox::indicator:checked {
                background-color: #1bb0b0; /* Color de fondo del indicador cuando se selecciona */
            }
        """)
        self.exento_check.setObjectName("exento_check")

        self.Button_guardar = QtWidgets.QPushButton(self)
        self.Button_guardar.setGeometry(QtCore.QRect(4, 264, 106, 31))
        self.Button_guardar.setStyleSheet("QPushButton {\n"
        "                background-color: #008080; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: none; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #008080; /* Color cuando se presiona el botón */\n"
        "            }\n"
        "            QPushButton:disabled {\n"
        "                background-color: #ccc; /* Color cuando el botón está deshabilitado */\n"
        "            }")
        self.Button_guardar.setObjectName("Button_guardar")
        #self.Button_guardar.clicked.connect(self.guardar_impuestos)

        self.Button_salir = QtWidgets.QPushButton(self)
        self.Button_salir.setGeometry(QtCore.QRect(117, 264, 106, 31))
        self.Button_salir.setStyleSheet("QPushButton {\n"
        "                background-color: #ef0404; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: none; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #ef0404; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #af0000; /* Color cuando se presiona el botón */\n"
        "            }\n"
        "            QPushButton:disabled {\n"
        "                background-color: #ccc; /* Color cuando el botón está deshabilitado */\n"
        "            }")
        self.Button_salir.setObjectName("Button_salir")
        self.Button_salir.clicked.connect(self.close_dialog)

        self.fondo_descripcion = QtWidgets.QListView (self)
        self.fondo_descripcion.setGeometry(QtCore.QRect(3, 3, 221, 26))
        self.fondo_descripcion.setStyleSheet("background-color: rgb(0, 128, 128);")
        self.fondo_descripcion.setObjectName("fondo_descripcion")

        self.descripcion_label = QtWidgets.QLabel(self)
        self.descripcion_label.setGeometry(QtCore.QRect(25, 5, 181, 21))
        self.descripcion_label.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font: 63 10pt \"Montserrat SemiBold\";")
        self.descripcion_label.setObjectName("descripcion_label")

        #self.actualizar_checkboxes()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Seleccion_impuestos", "Selección Impuestos"))
        self.setWindowIcon(QIcon('icono.png'))  # Agrega el icono a la ventana
        self.iva_check.setText(_translate("Seleccion_impuestos", "I.V.A (16%)"))
        self.iva_percibido_check.setText(_translate("Seleccion_impuestos", "IVA PERCIBIDO"))
        self.ial_check.setText(_translate("Seleccion_impuestos", "I.A.L"))
        self.igtf_check.setText(_translate("Seleccion_impuestos", "I.G.T.F (3%)"))
        self.exento_check.setText(_translate("Seleccion_impuestos", "Exento (0%)"))
        self.Button_guardar.setText(_translate("Seleccion_impuestos", "Guardar"))
        self.Button_salir.setText(_translate("Seleccion_impuestos", "Salir"))
        self.descripcion_label.setText(_translate("Seleccion_impuestos", "Descripción del Impuesto"))

    def close_dialog(self):
        self.reject()  # Cierra el diálogo

    def actualizar_checkboxes(self):
        # Si es un nuevo producto, selecciona el IVA por defecto
        if self.es_nuevo_producto:
            self.iva_check.setChecked(True)  # Selecciona el IVA por defecto
        else:
            for impuesto in self.impuestos:
                if impuesto["nombre"] in self.impuestos_predeterminados:
                    if self.impuestos_predeterminados[impuesto["nombre"]]:
                        # Marca el checkbox si el impuesto está seleccionado
                        if impuesto["nombre"] == "IMPUESTO AL VALOR AGREGADO (IVA 16%)":
                            self.iva_check.setChecked(True)
                        elif impuesto["nombre"] == "IVA PERCIBIDO":
                            self.iva_percibido_check.setChecked(True)
                        elif impuesto["nombre"] == "I.A.L":
                            self.ial_check.setChecked(True)
                        elif impuesto["nombre"] == "IGTF":
                            self.igtf_check.setChecked(True)
                        elif impuesto["nombre"] == "EXENTO":
                            self.exento_check.setChecked(True)
                else:
                    # Si no está en los impuestos predeterminados, asegúrate de desmarcarlo
                    if impuesto["nombre"] == "IMPUESTO AL VALOR AGREGADO (IVA 16%)":
                        self.iva_check.setChecked(False)
                    elif impuesto["nombre"] == "IVA PERCIBIDO":
                        self.iva_percibido_check.setChecked(False)
                    elif impuesto["nombre"] == "I.A.L":
                        self.ial_check.setChecked(False)
                    elif impuesto["nombre"] == "IGTF":
                        self.igtf_check.setChecked(False)
                    elif impuesto["nombre"] == "EXENTO":
                        self.exento_check.setChecked(False)

        # Si es un producto existente, no selecciones el IVA por defecto
        if not self.es_nuevo_producto:
            self.iva_check.setChecked(self.impuestos_predeterminados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False))

    def obtener_impuestos_seleccionados(self):
        impuestos_seleccionados = {
            "IMPUESTO AL VALOR AGREGADO (IVA 16%)": self.iva_check.isChecked(),
            "IVA PERCIBIDO": self.iva_percibido_check.isChecked(),
            "I.A.L": self.ial_check.isChecked(),
            "IGTF": self.igtf_check.isChecked(),
            "EXENTO": self.exento_check.isChecked()
        }
        return impuestos_seleccionados
    
    def configurar_checkboxes(self):
        # Establecer el checkbox de impuesto como seleccionado por defecto
        if self.impuestos:  # Verifica que haya impuestos disponibles
            self.iva_check.setChecked(True)  # Por ejemplo, seleccionando IVA

    #def actualizar_checkboxes(self):
        for impuesto in self.impuestos:
            if impuesto["nombre"] == "IMPUESTO AL VALOR AGREGADO (IVA 16%)":
                self.iva_check.setChecked(impuesto["activo"])
            elif impuesto["nombre"] == "IVA PERCIBIDO":
                self.iva_percibido_check.setChecked(impuesto["activo"])
            elif impuesto["nombre"] == "I.A.L":
                self.ial_check.setChecked(impuesto["activo"])
            elif impuesto["nombre"] == "IGTF":
                self.igtf_check.setChecked(impuesto["activo"])
            elif impuesto["nombre"] == "EXENTO":
                self.exento_check.setChecked(impuesto["activo"])

    #def guardar_impuestos(self):
        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Actualizar el estado de cada impuesto según el checkbox
        impuestos = {
            "IMPUESTO AL VALOR AGREGADO (IVA 16%)": self.iva_check.isChecked(),
            "IVA PERCIBIDO": self.iva_percibido_check.isChecked(),
            "I.A.L": self.ial_check.isChecked(),
            "IGTF": self.igtf_check.isChecked(),
            "EXENTO": self.exento_check.isChecked(),
        }

        for nombre, activo in impuestos.items():
            # Verificar el estado actual en la base de datos
            cursor.execute("SELECT activo FROM impuestos WHERE nombre = ?", (nombre,))
            resultado = cursor.fetchone()

            if resultado is not None:
                # Si el estado ha cambiado, actualizar
                if resultado[0] != int(activo):
                    cursor.execute("UPDATE impuestos SET activo = ? WHERE nombre = ?", (int(activo), nombre))

        # Hacer commit de los cambios
        conn.commit()
        conn.close()

        self.accept()  # Cierra el diálogo

class CrearProductos(QMainWindow):
    def __init__(self, es_nuevo_producto=True):
        super().__init__()
        self.es_nuevo_producto = es_nuevo_producto
        self.impuestos_seleccionados = {
            "IMPUESTO AL VALOR AGREGADO (IVA 16%)": True,  # Establecer IVA como seleccionado por defecto
            "IVA PERCIBIDO": False,
            "I.A.L": False,
            "IGTF": False,
            "EXENTO": False
        }
        self.productos_impuestos = {}  # Diccionario para almacenar impuestos por producto
        self.cargar_impuestos()  # Cargar impuestos al iniciar
        self.imagen_scene = QGraphicsScene()
        self.setupUi(self)
        self.cargar_productos_en_tabla()
        self.cargar_marcas()
        self.cargar_linea()
        self.cargar_deposito()
        self.costo_actual_calculado = False
        
    conn = sqlite3.connect('Usuarios.db') 
    cursor = conn.cursor()

    def setupUi(self, MainWindow):
        self.setWindowTitle("Crear Productos")
        MainWindow.setFixedSize(1114, 660)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("Crear Productos")

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Creamos el QLineEdit para el código
        self.codigo_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.producto_creado = False
        self.codigo_edit.setGeometry(QtCore.QRect(25, 50, 120, 25))
        self.codigo_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.codigo_edit.setText("")
        self.codigo_edit.setObjectName("codigo_edit")
        self.codigo_edit.editingFinished.connect(lambda: self.mostrar_mensaje_estado(self.codigo_edit, "Ingrese el código del producto"))
        # Conectar el evento de "enter" en el campo de código
        self.codigo_edit.returnPressed.connect(self.verificar_codigo)
        # Conectar el evento de texto cambiado para convertir a mayúsculas
        self.codigo_edit.textChanged.connect(self.convertir_a_mayusculas)

        # Creamos el QLabel para el código
        self.codigo_label = QtWidgets.QLabel(self.centralwidget)
        self.codigo_label.setGeometry(QtCore.QRect(26, 35, 47, 13))
        self.codigo_label.setObjectName("codigo_label")

        # Creamos el QLineEdit para la descripcion
        self.descripcion_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.descripcion_edit.setGeometry(QtCore.QRect(25, 80, 410, 28))
        self.set_moneda_placeholder(self.descripcion_edit, 'Descripción del producto')
        self.descripcion_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.descripcion_edit.setObjectName("descripcion_edit")
        self.descripcion_edit.editingFinished.connect(lambda: self.mostrar_mensaje_estado(self.descripcion_edit, "Ingrese una descripción del producto"))

        # Creamos el combobox para las marca
        self.marca_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.marca_comboBox.setGeometry(QtCore.QRect(25, 130, 250, 22))
        self.marca_comboBox.setStyleSheet("""
            QComboBox::drop-down {
                background-color: #008080; /* Color de fondo del botón desplegable */
            }
            QComboBox::item:selected {
                background-color: #1bb0b0; /* Color de fondo del elemento seleccionado */
                color: white;              /* Color de texto del elemento seleccionado */
            }
        """)
        self.marca_comboBox.currentTextChanged.connect(self.abrir_ventana_marcas)

        # Creamos el combobox para las marca
        self.marca_label = QtWidgets.QLabel(self.centralwidget)
        self.marca_label.setGeometry(QtCore.QRect(25, 113, 47, 13))
        self.marca_label.setObjectName("marca_label")

        self.linea_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.linea_comboBox.setGeometry(QtCore.QRect(24, 177, 250, 22))
        self.linea_comboBox.setStyleSheet("""
            QComboBox::drop-down {
                background-color: #008080; /* Color de fondo del botón desplegable */
                color: white;              /* Color de texto del botón desplegable */
            }
            QComboBox::item {
                background-color: white;   /* Color de fondo de los elementos */
                color: black;              /* Color de texto de los elementos */
            }
            QComboBox::item:selected {
                background-color: #1bb0b0; /* Color de fondo del elemento seleccionado */
                color: white;              /* Color de texto del elemento seleccionado */
            }
        """)
        self.linea_comboBox.currentTextChanged.connect(self.abrir_ventana_linea)


        self.linea_label = QtWidgets.QLabel(self.centralwidget)
        self.linea_label.setGeometry(QtCore.QRect(25, 160, 101, 16))
        self.linea_label.setObjectName("linea_label")


        self.unidad_label = QtWidgets.QLabel(self.centralwidget)
        self.unidad_label.setGeometry(QtCore.QRect(400, 117, 47, 13))
        self.unidad_label.setObjectName("unidad_label")


        self.unidad_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.unidad_edit.setGeometry(QtCore.QRect(400, 131, 35, 25))
        self.unidad_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.unidad_edit.setValidator(QIntValidator()) # Establece el validador de enteros
        self.unidad_edit.setObjectName("unidad_edit")
        self.unidad_edit.editingFinished.connect(lambda: self.mostrar_mensaje_estado(self.unidad_edit, "Ingrese la unidad del producto"))


        self.paquete_label = QtWidgets.QLabel(self.centralwidget)
        self.paquete_label.setGeometry(QtCore.QRect(290, 117, 47, 13))
        self.paquete_label.setObjectName("paquete_label")


        self.paquete_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.paquete_edit.setGeometry(QtCore.QRect(290, 131, 40, 25))
        self.paquete_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.paquete_edit.setObjectName("paquete_edit")


        self.costo_moneda_local_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.costo_moneda_local_groupBox.setGeometry(QtCore.QRect(23, 210, 241, 131))
        self.costo_moneda_local_groupBox.setStyleSheet("QGroupBox {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")


        self.costo_anterior_label = QtWidgets.QLabel(self.costo_moneda_local_groupBox)
        self.costo_anterior_label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.costo_anterior_label.setObjectName("costo_anterior_label")


        self.costo_anterior_edit = QtWidgets.QLineEdit(self.costo_moneda_local_groupBox)
        self.costo_anterior_edit.setGeometry(QtCore.QRect(10, 40, 91, 25))
        self.costo_anterior_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.costo_anterior_edit.setValidator(MathValidator())
        self.set_moneda_placeholder(self.costo_anterior_edit, 'Bs.')
        self.costo_anterior_edit.setObjectName("costo_anterior_edit")
        self.costo_anterior_edit.editingFinished.connect(lambda: self.calcular_costo(self.costo_anterior_edit))
        self.costo_anterior_edit.editingFinished.connect(lambda: self.mostrar_mensaje_estado(self.costo_anterior_edit, "Ingrese el costo anterior del producto"))

        
        self.costo_actual_label = QtWidgets.QLabel(self.costo_moneda_local_groupBox)
        self.costo_actual_label.setGeometry(QtCore.QRect(10, 70, 71, 16))
        self.costo_actual_label.setObjectName("costo_actual_label")


        self.costo_actual_edit = QtWidgets.QLineEdit(self.costo_moneda_local_groupBox)
        self.costo_actual_edit.setGeometry(QtCore.QRect(10, 90, 91, 25))
        self.costo_actual_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.costo_actual_edit.setText("")
        self.costo_actual_edit.setValidator(MathValidator())
        self.set_moneda_placeholder(self.costo_actual_edit, 'Bs.')
        self.costo_actual_edit.setObjectName("costo_actual_edit")
        self.costo_actual_edit.editingFinished.connect(lambda: self.calcular_costo(self.costo_actual_edit))
        self.costo_actual_edit.editingFinished.connect(lambda: self.mostrar_mensaje_estado(self.costo_actual_edit, "Ingrese el costo actual del producto"))

        
        self.costo_promedio_edit = QtWidgets.QLineEdit(self.costo_moneda_local_groupBox)
        self.costo_promedio_edit.setGeometry(QtCore.QRect(120, 40, 91, 25))
        self.costo_promedio_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.costo_promedio_edit.setValidator(MathValidator())
        self.set_moneda_placeholder(self.costo_promedio_edit, 'Bs.')
        self.costo_promedio_edit.setObjectName("costo_promedio_edit")
        self.costo_promedio_edit.editingFinished.connect(lambda: self.calcular_costo(self.costo_promedio_edit))
        self.costo_promedio_edit.editingFinished.connect(lambda: self.mostrar_mensaje_estado(self.costo_promedio_edit, "Ingrese el costo promedio del producto"))

        self.costo_promedio_label = QtWidgets.QLabel(self.costo_moneda_local_groupBox)
        self.costo_promedio_label.setGeometry(QtCore.QRect(120, 20, 81, 16))
        self.costo_promedio_label.setObjectName("costo_promedio_label")


        self.costo_reposicion_edit = QtWidgets.QLineEdit(self.costo_moneda_local_groupBox)
        self.costo_reposicion_edit.setGeometry(QtCore.QRect(120, 90, 91, 25))
        self.costo_reposicion_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.costo_reposicion_edit.setValidator(MathValidator())
        self.set_moneda_placeholder(self.costo_reposicion_edit, 'Bs.')
        self.costo_reposicion_edit.setObjectName("costo_reposicion_edit")
        self.costo_reposicion_edit.editingFinished.connect(lambda: self.calcular_costo(self.costo_reposicion_edit))
        self.costo_reposicion_edit.editingFinished.connect(lambda: self.mostrar_mensaje_estado(self.costo_reposicion_edit, "Ingrese el costo de reposición del producto"))


        self.costo_reposicion_label = QtWidgets.QLabel(self.costo_moneda_local_groupBox)
        self.costo_reposicion_label.setGeometry(QtCore.QRect(120, 70, 91, 16))
        self.costo_reposicion_label.setObjectName("costo_reposicion_label")


        self.costo_moneda_referencial_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.costo_moneda_referencial_groupBox.setGeometry(QtCore.QRect(280, 210, 161, 131))
        self.costo_moneda_referencial_groupBox.setStyleSheet("QGroupBox {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.costo_moneda_referencial_groupBox.setObjectName("costo_moneda_referencial_groupBox")


        self.moneda_referencial_label = QtWidgets.QLabel(self.costo_moneda_referencial_groupBox)
        self.moneda_referencial_label.setGeometry(QtCore.QRect(10, 20, 101, 16))
        self.moneda_referencial_label.setObjectName("moneda_referencial_label")


        self.moneda_referencial_edit = QtWidgets.QLineEdit(self.costo_moneda_referencial_groupBox)
        self.moneda_referencial_edit.setGeometry(QtCore.QRect(10, 40, 113, 25))
        self.moneda_referencial_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #1bb0b0; /* Color de fondo */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #ffffff; /* Color del texto blanco */\n"
        "                font-weight: bold;\n"
        "            }")
        self.moneda_referencial_edit.setObjectName("moneda_referencial_edit")


        self.costo_actual_referencial_edit = QtWidgets.QLineEdit(self.costo_moneda_referencial_groupBox)
        self.costo_actual_referencial_edit.setGeometry(QtCore.QRect(10, 90, 113, 25))
        self.costo_actual_referencial_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.costo_actual_referencial_edit.setValidator(MathValidator())
        self.set_moneda_placeholder(self.costo_actual_referencial_edit, '$')
        self.costo_actual_referencial_edit.setObjectName("costo_actual_referencial_edit")
        self.costo_actual_referencial_edit.textChanged.connect(self.restablecer_valor_predeterminado)
        self.costo_actual_referencial_edit.editingFinished.connect(lambda: self.calcular_costo(self.costo_actual_referencial_edit))
        self.costo_actual_referencial_edit.editingFinished.connect(lambda: self.mostrar_mensaje_estado(self.costo_actual_referencial_edit, "Ingrese el costo actual de referencia del producto"))
        self.costo_actual_referencial_edit.editingFinished.connect(self.actualizar_costo_actual)


        self.costo_actual_referencial_label = QtWidgets.QLabel(self.costo_moneda_referencial_groupBox)
        self.costo_actual_referencial_label.setGeometry(QtCore.QRect(10, 70, 71, 16))
        self.costo_actual_referencial_label.setObjectName("costo_actual_referencial_label")


        self.tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_widget.setGeometry(QtCore.QRect(10, 0, 1091, 791))
        self.tab_widget.tabBar().setStyleSheet("""
            QTabBar::tab {
            background-color: #008080; /* Color de fondo de las pestañas */
            border: 0.5px solid #ccc; /* Borde de las pestañas */
            padding: 5px; /* Espacio entre el texto y el borde */
            color: #ffffff;
            }
        """)
        self.tab_widget.setAutoFillBackground(False)
        self.tab_widget.setInputMethodHints(QtCore.Qt.ImhNone)
        self.tab_widget.setObjectName("tab_widget")


        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")


        self.imagen_producto_graphicsView = QtWidgets.QGraphicsView(self.tab_6)
        self.imagen_producto_graphicsView.setGeometry(QtCore.QRect(890, 41, 151, 181))
        self.imagen_producto_graphicsView.setStyleSheet("QGraphicsView {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.imagen_producto_graphicsView.setScene(self.imagen_scene)
        self.imagen_producto_graphicsView.setFixedSize(190, 200)
        self.imagen_producto_graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.imagen_producto_graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        
        self.precios_tab = QtWidgets.QTabWidget(self.tab_6)
        self.precios_tab.setGeometry(QtCore.QRect(435, 20, 454, 300))
        self.precios_tab.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.precios_tab.setObjectName("precios_tab")


        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")


        self.moneda_listView = QtWidgets.QListView(self.tab_3)
        self.moneda_listView.setGeometry(QtCore.QRect(11, 10, 71, 25))
        self.moneda_listView.setStyleSheet("QListView {\n"
        "                background-color: #1bb0b0; /* Color de fondo negro */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #ffffff; /* Color del texto negro */\n"
        "                font-weight: bold;\n"
        "            }")
        self.moneda_list_model = QStandardItemModel(self.moneda_listView)
        self.moneda_listView.setModel(self.moneda_list_model)

        item = QStandardItem("Bolivares")
        self.moneda_list_model.appendRow(item)


        self.utilidad_bs_label = QtWidgets.QLabel(self.tab_3)
        self.utilidad_bs_label.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.utilidad_bs_label.setObjectName("utilidad_bs_label")

        self.utilidad_bs_edit = QtWidgets.QLineEdit(self.tab_3)
        self.utilidad_bs_edit.setGeometry(QtCore.QRect(10, 60, 111, 25))
        self.utilidad_bs_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        regex = QRegExp("^[0-9]+([\\.,][0-9]+)?%?$")
        self.utilidad_bs_edit.setValidator(QRegExpValidator(regex))

        self.precio_sin_impuesto_bs_label = QtWidgets.QLabel(self.tab_3)
        self.precio_sin_impuesto_bs_label.setGeometry(QtCore.QRect(10, 87, 101, 16))
        self.precio_sin_impuesto_bs_label.setObjectName("precio_sin_impuesto_bs_label")


        self.precio_sin_impuesto_bs_edit = QtWidgets.QLineEdit(self.tab_3)
        self.precio_sin_impuesto_bs_edit.setGeometry(QtCore.QRect(10, 105, 111, 25))
        self.precio_sin_impuesto_bs_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_sin_impuesto_bs_edit.setValidator(QDoubleValidator())
        self.precio_sin_impuesto_bs_edit.setValidator(MathValidator())
        self.precio_sin_impuesto_bs_edit.setObjectName("precio_sin_impuesto_bs_edit")

        self.impuesto_total_bs_label = QtWidgets.QLabel(self.tab_3)
        self.impuesto_total_bs_label.setGeometry(QtCore.QRect(10, 133, 81, 16))
        self.impuesto_total_bs_label.setObjectName("impuesto_total_bs_label")


        self.impuesto_total_bs_edit = QtWidgets.QLineEdit(self.tab_3)
        self.impuesto_total_bs_edit.setGeometry(QtCore.QRect(10, 153, 111, 25))
        self.impuesto_total_bs_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.impuesto_total_bs_edit.setValidator(QDoubleValidator())
        self.impuesto_total_bs_edit.setValidator(MathValidator())
        self.impuesto_total_bs_edit.setObjectName("impuesto_total_bs_edit")


        self.precio_total_bs_label = QtWidgets.QLabel(self.tab_3)
        self.precio_total_bs_label.setGeometry(QtCore.QRect(10, 180, 61, 16))
        self.precio_total_bs_label.setObjectName("precio_total_bs_label")


        self.precio_total_bs_edit = QtWidgets.QLineEdit(self.tab_3)
        self.precio_total_bs_edit.setGeometry(QtCore.QRect(10, 200, 113, 25))
        self.precio_total_bs_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_total_bs_edit.setValidator(QDoubleValidator())
        self.precio_total_bs_edit.setValidator(MathValidator())
        self.precio_total_bs_edit.setObjectName("precio_total_bs_edit")


        self.lineEdit_17 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_17.setGeometry(QtCore.QRect(144, 60, 91, 25))
        self.lineEdit_17.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_total_bs_edit.setValidator(QDoubleValidator())
        self.lineEdit_17.setValidator(MathValidator())
        self.lineEdit_17.setObjectName("Resultado utilidad bs")


        self.linea_bs_line = QtWidgets.QFrame(self.tab_3)
        self.linea_bs_line.setGeometry(QtCore.QRect(127, 61, 16, 21))
        self.linea_bs_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.linea_bs_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.linea_bs_line.setObjectName("linea_bs_line")

        self.linea_bs_dolar_line = QtWidgets.QFrame(self.tab_3)
        self.linea_bs_dolar_line.setGeometry(QtCore.QRect(258, 30, 16, 211))
        self.linea_bs_dolar_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.linea_bs_dolar_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.linea_bs_dolar_line.setObjectName("linea_bs_dolar_line")


        self.bs_label = QtWidgets.QLabel(self.tab_3)
        self.bs_label.setGeometry(QtCore.QRect(240, 64, 21, 16))
        self.bs_label.setObjectName("bs_label")


        self.utilidad_dolar_edit = QtWidgets.QLineEdit(self.tab_3)
        self.utilidad_dolar_edit.setGeometry(QtCore.QRect(290, 60, 111, 25))
        self.utilidad_dolar_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.utilidad_dolar_edit.setValidator(MathValidator())
        self.utilidad_dolar_edit.setValidator(QDoubleValidator())
        self.utilidad_dolar_edit.returnPressed.connect(self.on_return_pressed)


        self.precio_dolar_sin_impuesto_edit = QtWidgets.QLineEdit(self.tab_3)
        self.precio_dolar_sin_impuesto_edit.setGeometry(QtCore.QRect(290, 110, 111, 25))
        self.precio_dolar_sin_impuesto_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_dolar_sin_impuesto_edit.setValidator(QDoubleValidator())
        self.precio_dolar_sin_impuesto_edit.setValidator(MathValidator())
        regex = QRegExp("^[0-9]+([\\.,][0-9]+)?%?$")
        self.precio_dolar_sin_impuesto_edit.setObjectName("precio_dolar_sin_impuesto_edit")


        self.precio_dolar_sin_impuesto_label = QtWidgets.QLabel(self.tab_3)
        self.precio_dolar_sin_impuesto_label.setGeometry(QtCore.QRect(290, 90, 101, 16))
        self.precio_dolar_sin_impuesto_label.setObjectName("precio_dolar_sin_impuesto_label")


        self.precio_total_dolar_label = QtWidgets.QLabel(self.tab_3)
        self.precio_total_dolar_label.setGeometry(QtCore.QRect(290, 140, 61, 16))
        self.precio_total_dolar_label.setObjectName("precio_total_dolar_label")


        self.precio_total_dolar_edit = QtWidgets.QLineEdit(self.tab_3)
        self.precio_total_dolar_edit.setGeometry(QtCore.QRect(290, 160, 113, 25))
        self.precio_total_dolar_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_total_dolar_edit.setValidator(QDoubleValidator())
        self.precio_total_dolar_edit.setValidator(MathValidator())
        regex = QRegExp("^[0-9]+([\\.,][0-9]+)?%?$")
        self.precio_total_dolar_edit.setObjectName("precio_total_dolar_edit")
        self.precio_total_dolar_edit.editingFinished.connect(lambda: self.calcular_costo(self.precio_total_dolar_edit))
        self.precio_total_dolar_edit.textChanged.connect(self.calcular_utilidad_y_impuesto)

        self.utilidad_dolar_label = QtWidgets.QLabel(self.tab_3)
        self.utilidad_dolar_label.setGeometry(QtCore.QRect(290, 40, 47, 13))
        self.utilidad_dolar_label.setObjectName("utilidad_dolar_label")


        self.moneda_ref_listView = QtWidgets.QListView(self.tab_3)
        self.moneda_ref_listView.setGeometry(QtCore.QRect(290, 10, 71, 25))
        self.moneda_ref_listView.setStyleSheet("QListView {\n"
        "                background-color: #1bb0b0; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #ffffff; /* Color del texto negro */\n"
        "                font-weight: bold;"
        "            }")
        self.moneda_ref_list_model = QStandardItemModel(self.moneda_ref_listView)
        self.moneda_ref_listView.setModel(self.moneda_ref_list_model)

        item = QStandardItem("Dolares")
        self.moneda_ref_list_model.appendRow(item)

        self.precios_tab.addTab(self.tab_3, "")
        self.precios_tab.tabBar().setStyleSheet("""
            QTabBar::tab {
            background-color: #008080; /* Color de fondo de las pestañas */
            border: 0.5px solid #ccc; /* Borde de las pestañas */
            padding: 5px; /* Espacio entre el texto y el borde */
            color: #ffffff;
            }
            QTabBar::tab:selected {
            background-color: #1bb0b0; /* Color de fondo de la pestaña seleccionada */
            color: #ffffff; /* Color del texto de la pestaña seleccionada */
            }
        """)

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.precio_sin_impuesto_bs_label_2 = QtWidgets.QLabel(self.tab)
        self.precio_sin_impuesto_bs_label_2.setGeometry(QtCore.QRect(10, 87, 101, 16))
        self.precio_sin_impuesto_bs_label_2.setObjectName("precio_sin_impuesto_bs_label_2")


        self.precio_sin_impuesto_bs_edit_2 = QtWidgets.QLineEdit(self.tab)
        self.precio_sin_impuesto_bs_edit_2.setGeometry(QtCore.QRect(10, 105, 111, 25))
        self.precio_sin_impuesto_bs_edit_2.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_sin_impuesto_bs_edit_2.setValidator(QDoubleValidator())
        self.precio_sin_impuesto_bs_edit_2.setValidator(MathValidator())
        self.precio_sin_impuesto_bs_edit_2.setObjectName("precio_sin_impuesto_bs_edit_2")
        
        self.impuesto_total_bs_edit_2 = QtWidgets.QLineEdit(self.tab)
        self.impuesto_total_bs_edit_2.setGeometry(QtCore.QRect(10, 153, 111, 25))
        self.impuesto_total_bs_edit_2.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.impuesto_total_bs_edit_2.setValidator(MathValidator())
        self.impuesto_total_bs_edit_2.setObjectName("impuesto_total_bs_edit_2")


        self.precio_total_bs_label_2 = QtWidgets.QLabel(self.tab)
        self.precio_total_bs_label_2.setGeometry(QtCore.QRect(10, 180, 61, 16))
        self.precio_total_bs_label_2.setObjectName("precio_total_bs_label_2")


        self.precio_total_bs_edit_2 = QtWidgets.QLineEdit(self.tab)
        self.precio_total_bs_edit_2.setGeometry(QtCore.QRect(10, 200, 113, 25))
        self.precio_total_bs_edit_2.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_total_bs_edit_2.setValidator(MathValidator())
        self.precio_total_bs_edit_2.setObjectName("precio_total_bs_edit_2")


        self.bs_label_2 = QtWidgets.QLabel(self.tab)
        self.bs_label_2.setGeometry(QtCore.QRect(240, 64, 21, 16))
        self.bs_label_2.setObjectName("bs_label_2")


        self.utilidad_bs_edit_2 = QtWidgets.QLineEdit(self.tab)
        self.utilidad_bs_edit_2.setGeometry(QtCore.QRect(10, 60, 111, 25))
        self.utilidad_bs_edit_2.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        regex = QRegExp("^[0-9]+([\\.,][0-9]+)?%?$")
        self.utilidad_bs_edit_2.setValidator(QRegExpValidator(regex))
        self.utilidad_bs_edit_2.setValidator(MathValidator())


        self.linea_bs_dolar_line_2 = QtWidgets.QFrame(self.tab)
        self.linea_bs_dolar_line_2.setGeometry(QtCore.QRect(258, 30, 16, 211))
        self.linea_bs_dolar_line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.linea_bs_dolar_line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.linea_bs_dolar_line_2.setObjectName("linea_bs_dolar_line_2")


        self.linea_bs_line_2 = QtWidgets.QFrame(self.tab)
        self.linea_bs_line_2.setGeometry(QtCore.QRect(127, 61, 16, 21))
        self.linea_bs_line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.linea_bs_line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.linea_bs_line_2.setObjectName("linea_bs_line_2")


        self.precio_total_dolar_edit_2 = QtWidgets.QLineEdit(self.tab)
        self.precio_total_dolar_edit_2.setGeometry(QtCore.QRect(290, 160, 113, 25))
        self.precio_total_dolar_edit_2.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_total_dolar_edit_2.setValidator(MathValidator())
        self.precio_total_dolar_edit_2.setObjectName("precio_total_dolar_edit_2")
        self.precio_total_dolar_edit_2.textChanged.connect(self.calcular_utilidad_y_impuesto_2)

        
        self.precio_dolar_sin_impuesto_label_2 = QtWidgets.QLabel(self.tab)
        self.precio_dolar_sin_impuesto_label_2.setGeometry(QtCore.QRect(290, 90, 101, 16))
        self.precio_dolar_sin_impuesto_label_2.setObjectName("precio_dolar_sin_impuesto_label_2")


        self.lineEdit_18 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_18.setGeometry(QtCore.QRect(144, 60, 91, 25))
        self.lineEdit_18.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.lineEdit_18.setValidator(MathValidator())
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.lineEdit_18.textChanged.connect(lambda: self.calcular_costo(self.lineEdit_18))


        self.utilidad_bs_label_2 = QtWidgets.QLabel(self.tab)
        self.utilidad_bs_label_2.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.utilidad_bs_label_2.setObjectName("utilidad_bs_label_2")


        self.impuesto_total_bs_label_2 = QtWidgets.QLabel(self.tab)
        self.impuesto_total_bs_label_2.setGeometry(QtCore.QRect(10, 133, 81, 16))
        self.impuesto_total_bs_label_2.setObjectName("impuesto_total_bs_label_2")


        self.moneda_listView_2 = QtWidgets.QListView(self.tab)
        self.moneda_listView_2.setGeometry(QtCore.QRect(11, 10, 71, 25))
        self.moneda_listView_2.setStyleSheet("QListView {\n"
        "                background-color: #1bb0b0; /* Color de fondo */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #ffffff; /* Color del texto blanco */\n"
        "                font-weight: bold;\n"
        "            }")
        self.moneda_list2_model = QStandardItemModel(self.moneda_listView_2)
        self.moneda_listView_2.setModel(self.moneda_list2_model)

        item = QStandardItem("Bolivares")
        self.moneda_list2_model.appendRow(item)


        self.precio_dolar_sin_impuesto_edit_2 = QtWidgets.QLineEdit(self.tab)
        self.precio_dolar_sin_impuesto_edit_2.setGeometry(QtCore.QRect(290, 110, 111, 25))
        self.precio_dolar_sin_impuesto_edit_2.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_dolar_sin_impuesto_edit_2.setValidator(MathValidator())
        self.precio_dolar_sin_impuesto_edit_2.setObjectName("precio_dolar_sin_impuesto_edit_2")
        self.precio_dolar_sin_impuesto_edit_2.textChanged.connect(lambda: self.calcular_costo(self.precio_dolar_sin_impuesto_edit_2))

        self.moneda_ref_listView_2 = QtWidgets.QListView(self.tab)
        self.moneda_ref_listView_2.setGeometry(QtCore.QRect(290, 10, 71, 25))
        self.moneda_ref_listView_2.setStyleSheet("QListView {\n"
        "                background-color: #1bb0b0; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #ffffff; /* Color del texto negro */\n"
        "                font-weight: bold;"
        "            }")
        self.moneda_ref_list2_model = QStandardItemModel(self.moneda_ref_listView_2)
        self.moneda_ref_listView_2.setModel(self.moneda_ref_list2_model)

        item = QStandardItem("Dolares")
        self.moneda_ref_list2_model.appendRow(item)


        self.precio_total_dolar_label_2 = QtWidgets.QLabel(self.tab)
        self.precio_total_dolar_label_2.setGeometry(QtCore.QRect(290, 140, 61, 16))
        self.precio_total_dolar_label_2.setObjectName("precio_total_dolar_label_2")


        self.utilidad_dolar_edit_2 = QtWidgets.QLineEdit(self.tab)
        self.utilidad_dolar_edit_2.setGeometry(QtCore.QRect(290, 60, 111, 25))
        self.utilidad_dolar_edit_2.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.utilidad_dolar_edit_2.setValidator(MathValidator())
        self.utilidad_dolar_edit_2.setValidator(QDoubleValidator())
        regex = QRegExp("^[0-9]+([\\.,][0-9]+)?%?$")
        self.utilidad_dolar_edit_2.setValidator(QRegExpValidator(regex))
        self.utilidad_dolar_edit_2.returnPressed.connect(self.on_return_pressed_2)


        self.utilidad_dolar_label_2 = QtWidgets.QLabel(self.tab)
        self.utilidad_dolar_label_2.setGeometry(QtCore.QRect(290, 40, 47, 13))
        self.utilidad_dolar_label_2.setObjectName("utilidad_dolar_label_2")

        self.precios_tab.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")


        self.precio_sin_impuesto_bs_label_3 = QtWidgets.QLabel(self.tab_2)
        self.precio_sin_impuesto_bs_label_3.setGeometry(QtCore.QRect(10, 87, 101, 16))
        self.precio_sin_impuesto_bs_label_3.setObjectName("precio_sin_impuesto_bs_label_3")


        self.impuesto_total_bs_edit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.impuesto_total_bs_edit_3.setGeometry(QtCore.QRect(10, 153, 111, 25))
        self.impuesto_total_bs_edit_3.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.impuesto_total_bs_edit_3.setValidator(MathValidator())
        self.impuesto_total_bs_edit_3.setObjectName("impuesto_total_bs_edit_3")


        self.utilidad_dolar_edit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.utilidad_dolar_edit_3.setGeometry(QtCore.QRect(290, 60, 111, 25))
        self.utilidad_dolar_edit_3.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.utilidad_dolar_edit_3.setValidator(MathValidator())
        self.utilidad_dolar_edit_3.setValidator(QDoubleValidator())
        regex = QRegExp("^[0-9]+([\\.,][0-9]+)?%?$")
        self.utilidad_dolar_edit_3.setValidator(QRegExpValidator(regex))
        self.utilidad_dolar_edit_3.returnPressed.connect(self.on_return_pressed_3)


        self.precio_sin_impuesto_bs_edit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.precio_sin_impuesto_bs_edit_3.setGeometry(QtCore.QRect(10, 105, 111, 25))
        self.precio_sin_impuesto_bs_edit_3.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_sin_impuesto_bs_edit_3.setValidator(MathValidator())
        self.precio_sin_impuesto_bs_edit_3.setObjectName("precio_sin_impuesto_bs_edit_3")
        self.precio_sin_impuesto_bs_edit_3.textChanged.connect(lambda: self.calcular_costo(self.precio_sin_impuesto_bs_edit_3))


        self.linea_bs_line_3 = QtWidgets.QFrame(self.tab_2)
        self.linea_bs_line_3.setGeometry(QtCore.QRect(127, 61, 16, 21))
        self.linea_bs_line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.linea_bs_line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.linea_bs_line_3.setObjectName("linea_bs_line_3")


        self.utilidad_dolar_label_3 = QtWidgets.QLabel(self.tab_2)
        self.utilidad_dolar_label_3.setGeometry(QtCore.QRect(290, 40, 47, 13))
        self.utilidad_dolar_label_3.setObjectName("utilidad_dolar_label_3")


        self.precio_total_dolar_edit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.precio_total_dolar_edit_3.setGeometry(QtCore.QRect(290, 160, 113, 25))
        self.precio_total_dolar_edit_3.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_total_dolar_edit_3.setValidator(MathValidator())
        self.precio_total_dolar_edit_3.setObjectName("precio_total_dolar_edit_3")
        self.precio_total_dolar_edit_3.textChanged.connect(self.calcular_utilidad_y_impuesto_3)
        


        self.precio_total_dolar_label_3 = QtWidgets.QLabel(self.tab_2)
        self.precio_total_dolar_label_3.setGeometry(QtCore.QRect(290, 140, 61, 16))
        self.precio_total_dolar_label_3.setObjectName("precio_total_dolar_label_3")


        self.lineEdit_19 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_19.setGeometry(QtCore.QRect(144, 60, 91, 25))
        self.lineEdit_19.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.lineEdit_19.setValidator(MathValidator())
        self.lineEdit_19.textChanged.connect(lambda: self.calcular_costo(self.lineEdit_19))


        self.precio_total_bs_edit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.precio_total_bs_edit_3.setGeometry(QtCore.QRect(10, 200, 113, 25))
        self.precio_total_bs_edit_3.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_total_bs_edit_3.setValidator(MathValidator())
        self.precio_total_bs_edit_3.textChanged.connect(lambda: self.calcular_costo(self.precio_total_bs_edit_3))


        self.utilidad_bs_edit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.utilidad_bs_edit_3.setGeometry(QtCore.QRect(10, 60, 111, 25))
        self.utilidad_bs_edit_3.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.utilidad_bs_edit_3.setValidator(MathValidator())


        self.linea_bs_dolar_line_3 = QtWidgets.QFrame(self.tab_2)
        self.linea_bs_dolar_line_3.setGeometry(QtCore.QRect(258, 30, 16, 211))
        self.linea_bs_dolar_line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.linea_bs_dolar_line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.linea_bs_dolar_line_3.setObjectName("linea_bs_dolar_line_3")


        self.precio_dolar_sin_impuesto_label_3 = QtWidgets.QLabel(self.tab_2)
        self.precio_dolar_sin_impuesto_label_3.setGeometry(QtCore.QRect(290, 90, 101, 16))
        self.precio_dolar_sin_impuesto_label_3.setObjectName("precio_dolar_sin_impuesto_label_3")


        self.precio_total_bs_label_3 = QtWidgets.QLabel(self.tab_2)
        self.precio_total_bs_label_3.setGeometry(QtCore.QRect(10, 180, 61, 16))
        self.precio_total_bs_label_3.setObjectName("precio_total_bs_label_3")


        self.impuesto_total_bs_label_3 = QtWidgets.QLabel(self.tab_2)
        self.impuesto_total_bs_label_3.setGeometry(QtCore.QRect(10, 133, 81, 16))
        self.impuesto_total_bs_label_3.setObjectName("impuesto_total_bs_label_3")


        self.precio_dolar_sin_impuesto_edit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.precio_dolar_sin_impuesto_edit_3.setGeometry(QtCore.QRect(290, 110, 111, 25))
        self.precio_dolar_sin_impuesto_edit_3.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.precio_dolar_sin_impuesto_edit_3.setValidator(MathValidator())
        self.precio_dolar_sin_impuesto_edit_3.setObjectName("precio_dolar_sin_impuesto_edit_3")
        self.precio_dolar_sin_impuesto_edit_3.textChanged.connect(lambda: self.calcular_costo(self.precio_dolar_sin_impuesto_edit_3))

        self.moneda_ref_listView_3 = QtWidgets.QListView(self.tab_2)
        self.moneda_ref_listView_3.setGeometry(QtCore.QRect(290, 10, 71, 25))
        self.moneda_ref_listView_3.setStyleSheet("QListView {\n"
        "                background-color: #1bb0b0; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #ffffff; /* Color del texto negro */\n"
        "                font-weight: bold;"
        "            }")
        self.moneda_ref_list3_model = QStandardItemModel(self.moneda_ref_listView_3)
        self.moneda_ref_listView_3.setModel(self.moneda_ref_list3_model)

        item = QStandardItem("Dolares")
        self.moneda_ref_list3_model.appendRow(item)


        self.moneda_listView_3 = QtWidgets.QListView(self.tab_2)
        self.moneda_listView_3.setGeometry(QtCore.QRect(11, 10, 71, 25))
        self.moneda_listView_3.setStyleSheet("QListView {\n"
        "                background-color: #1bb0b0; /* Color de fondo */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #ffffff; /* Color del texto negro */\n"
        "                font-weight: bold;\n"
        "            }")
        self.moneda_list3_model = QStandardItemModel(self.moneda_listView_3)
        self.moneda_listView_3.setModel(self.moneda_list3_model)

        item = QStandardItem("Bolivares")
        self.moneda_list3_model.appendRow(item)


        self.utilidad_bs_label_3 = QtWidgets.QLabel(self.tab_2)
        self.utilidad_bs_label_3.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.utilidad_bs_label_3.setObjectName("utilidad_bs_label_3")

        self.bs_label_3 = QtWidgets.QLabel(self.tab_2)
        self.bs_label_3.setGeometry(QtCore.QRect(240, 64, 21, 16))
        self.bs_label_3.setObjectName("bs_label_3")

        self.precios_tab.addTab(self.tab_2, "")

        self.deposito_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.deposito_comboBox.setGeometry(QtCore.QRect(305, 51, 60, 22))
        self.deposito_comboBox.setStyleSheet("""
            QComboBox::drop-down {
                background-color: #008080; /* Color de fondo del botón desplegable */
                color: white;              /* Color de texto del botón desplegable */
            }
            QComboBox::item {
                background-color: white;   /* Color de fondo de los elementos */
                color: black;              /* Color de texto de los elementos */
            }
            QComboBox::item:selected {
                background-color: #1bb0b0; /* Color de fondo del elemento seleccionado */
                color: white;              /* Color de texto del elemento seleccionado */
            }
        """)

        self.activo_checkBox = QtWidgets.QCheckBox(self.tab_6)
        self.activo_checkBox.setGeometry(QtCore.QRect(360, 20, 70, 30))
        self.activo_checkBox.setStyleSheet("""
            QCheckBox {  
                border: none; 
                border-radius: 5px; 
                padding: 5px;
                color: #000000 
            }
            QCheckBox::indicator {
                width: 20px; /* Ancho del indicador */
                height: 20px; /* Alto del indicador */
                border: 1px solid #ccc; /* Borde del indicador */
                border-radius: 5px; /* Radio del borde del indicador */
                background-color: #fff; /* Color de fondo del indicador */
            }
            QCheckBox::indicator:checked {
                background-color: #1bb0b0; /* Color de fondo del indicador cuando se selecciona */
            }
        """)
        self.activo_checkBox.stateChanged.connect(self.cambiar_estado_activo)

        self.table_productos = QtWidgets.QTableWidget(self.tab_6)
        self.table_productos.setGeometry(QtCore.QRect(10, 365, 1071, 210))
        self.table_productos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_productos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_productos.setStyleSheet("QTableWidget::item:selected {\n"
        "                background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */\n"
        "                color: white; /* Color del texto de la fila seleccionada */\n"
        "            }\n"
        "            QHeaderView::section {\n"
        "                background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */\n"
        "                border: 5px;\n"
        "                color: #ffffff;\n"
        "            }")
        self.table_productos.verticalHeader().setVisible(False)
        self.table_productos.selectionModel().selectionChanged.connect(self.habilitar_eliminar)
        self.table_productos.selectionModel().selectionChanged.connect(self.mostrar_imagen_producto)

        self.table_productos.setColumnCount(6)
        self.table_productos.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_productos.setHorizontalHeaderItem(0, item)
        self.table_productos.setColumnWidth(0, 120)
        item = QtWidgets.QTableWidgetItem()
        self.table_productos.setHorizontalHeaderItem(1, item)
        self.table_productos.setColumnWidth(1, 569)  # Establece el ancho de la columna "Descripción" en 300 píxeles
        item = QtWidgets.QTableWidgetItem()
        self.table_productos.setHorizontalHeaderItem(2, item)
        self.table_productos.setColumnWidth(2, 120)
        item = QtWidgets.QTableWidgetItem()
        self.table_productos.setHorizontalHeaderItem(3, item)
        self.table_productos.setColumnWidth(3, 60)
        item = QtWidgets.QTableWidgetItem()
        self.table_productos.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_productos.setHorizontalHeaderItem(5, item)

        self.peso_litro_label = QtWidgets.QLabel(self.tab_6)
        self.peso_litro_label.setGeometry(QtCore.QRect(329, 91, 47, 13))
        self.peso_litro_label.setObjectName("peso_litro_label")

        self.peso_litro_edit = QtWidgets.QLineEdit(self.tab_6)
        self.peso_litro_edit.setGeometry(QtCore.QRect(329, 105, 50, 25))
        self.peso_litro_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.peso_litro_edit.setObjectName("Peso/Litro")


        self.existencia_maxima_edit = QtWidgets.QLineEdit(self.tab_6)
        self.existencia_maxima_edit.setGeometry(QtCore.QRect(360, 153, 62, 25))
        self.existencia_maxima_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.existencia_maxima_edit.setValidator(QIntValidator()) # Establece el validador de enteros
        self.existencia_maxima_edit.setObjectName("existencia_maxima_edit")


        self.existencia_maxima_label = QtWidgets.QLabel(self.tab_6)
        self.existencia_maxima_label.setGeometry(QtCore.QRect(358, 136, 81, 16))
        self.existencia_maxima_label.setObjectName("existencia_maxima_label")


        self.existencia_minima_edit = QtWidgets.QLineEdit(self.tab_6)
        self.existencia_minima_edit.setGeometry(QtCore.QRect(278, 153, 62, 25))
        self.existencia_minima_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.existencia_minima_edit.setValidator(QIntValidator()) # Establece el validador de enteros
        self.existencia_minima_edit.setObjectName("existencia_minima_edit")


        self.existencia_minima_label = QtWidgets.QLabel(self.tab_6)
        self.existencia_minima_label.setGeometry(QtCore.QRect(278, 136, 91, 16))
        self.existencia_minima_label.setObjectName("existencia_minima_label")


        self.codigo_barra_edit = QtWidgets.QLineEdit(self.tab_6)
        self.codigo_barra_edit.setGeometry(QtCore.QRect(140, 24, 140, 25))
        self.codigo_barra_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.codigo_barra_edit.setText("")
        self.codigo_barra_edit.setObjectName("codigo_barra_edit")


        self.codigo_barra_label = QtWidgets.QLabel(self.tab_6)
        self.codigo_barra_label.setGeometry(QtCore.QRect(140, 8, 81, 16))
        self.codigo_barra_label.setObjectName("codigo_barra_label")

        self.deposito_label = QtWidgets.QLabel(self.tab_6)
        self.deposito_label.setGeometry(QtCore.QRect(295, 8, 81, 16))
        self.deposito_label.setObjectName("deposito_label")


        self.buscar_producto_edit = QtWidgets.QLineEdit(self.tab_6)
        self.buscar_producto_edit.setGeometry(QtCore.QRect(10, 330, 271, 25))
        self.buscar_producto_edit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.buscar_producto_edit.setText("")
        self.buscar_producto_edit.setPlaceholderText("Buscar producto")
        self.buscar_producto_edit.textChanged.connect(self.filtrar_productos)  # Conectar la señal de texto cambiado

    


        self.imagen_producto_label = QtWidgets.QLabel(self.tab_6)
        self.imagen_producto_label.setGeometry(QtCore.QRect(940, 24, 101, 16))


        self.button_anadir = QtWidgets.QPushButton(self.tab_6)
        self.button_anadir.setGeometry(QtCore.QRect(925, 245, 61, 31))
        self.button_anadir.setStyleSheet("QPushButton {\n"
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
        self.button_anadir.clicked.connect(self.seleccionar_imagen)

        self.button_borrar = QtWidgets.QPushButton(self.tab_6)
        self.button_borrar.setGeometry(QtCore.QRect(990, 245, 61, 31))
        self.button_borrar.setStyleSheet("QPushButton {\n"
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
        self.button_borrar.clicked.connect(self.borrar_imagen)

        self.button_importar = QtWidgets.QPushButton(self.tab_6)
        self.button_importar.setGeometry(QtCore.QRect(678, 325, 110, 32))
        self.button_importar.setStyleSheet("QPushButton {\n"
        "                background-color: #008080; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: 5px; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #ef0404; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #aa0000; /* Color cuando se presiona el botón */\n"
        "            }\n"
        "            QPushButton:disabled {\n"
        "                background-color: #ccc; /* Color cuando el botón está deshabilitado */\n"
        "            }")
        self.button_importar.clicked.connect(self.importar_inventario)

        self.button_exportar = QtWidgets.QPushButton(self.tab_6)
        self.button_exportar.setGeometry(QtCore.QRect(557, 325, 110, 32))
        self.button_exportar.setStyleSheet("QPushButton {\n"
        "                background-color: #008080; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: 5px; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #ef0404; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #aa0000; /* Color cuando se presiona el botón */\n"
        "            }\n"
        "            QPushButton:disabled {\n"
        "                background-color: #ccc; /* Color cuando el botón está deshabilitado */\n"
        "            }")
        self.button_exportar.clicked.connect(self.exportar_inventario)

        self.button_etiqueta = QtWidgets.QPushButton(self.tab_6)
        self.button_etiqueta.setEnabled(False)
        self.button_etiqueta.setGeometry(QtCore.QRect(800, 325, 110, 32))
        self.button_etiqueta.setStyleSheet("QPushButton {\n"
        "                background-color: #008080; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: 5px; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #ef0404; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #aa0000; /* Color cuando se presiona el botón */\n"
        "            }\n"
        "            QPushButton:disabled {\n"
        "                background-color: #ccc; /* Color cuando el botón está deshabilitado */\n"
        "            }")
        self.button_etiqueta.clicked.connect(self.generar_etiqueta)
        # Etiqueta para mostrar el código de barras
        self.codigo_barras_label = QLabel()
        # Conectar la señal de selección de la tabla
        self.table_productos.itemSelectionChanged.connect(self.toggle_generar_etiqueta_button)


        self.button_ultimas_transacciones = QtWidgets.QPushButton(self.tab_6)
        self.button_ultimas_transacciones.setGeometry(QtCore.QRect(921, 325, 150, 32))
        self.button_ultimas_transacciones.setStyleSheet("QPushButton {\n"
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
        self.button_ultimas_transacciones.setObjectName("button_ultimas_transacciones")

        self.button_impuestos = QtWidgets.QPushButton(self.tab_6)
        self.button_impuestos.setGeometry(QtCore.QRect(450, 277, 75, 33))
        self.button_impuestos.setStyleSheet("QPushButton {\n"
        "                background-color: #008080; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: none; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #ef0404; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #aa0000; /* Color cuando se presiona el botón */\n"
        "            }\n"
        "            QPushButton:disabled {\n"
        "                background-color: #ccc; /* Color cuando el botón está deshabilitado */\n"
        "            }")
        self.button_impuestos.clicked.connect(self.abrir_seleccion_impuestos)

        self.tab_widget.addTab(self.tab_6, "")


        self.button_cerrar = QtWidgets.QPushButton(self.centralwidget)
        self.button_cerrar.setGeometry(QtCore.QRect(1010, 605, 75, 31))
        self.button_cerrar.setStyleSheet("QPushButton {\n"
        "                background-color: #008080; \n"
        "                color: #fff; \n"
        "                border: none; \n"
        "                border-radius: 5px; \n"
        "                padding: 10px;\n"
        "            }\n"
        "            QPushButton:hover {\n"
        "                background-color: #ef0404; /* Color cuando se coloca el cursor sobre el botón */\n"
        "            }\n"
        "            QPushButton:pressed {\n"
        "                background-color: #af0000; /* Color cuando se presiona el botón */\n"
        "            }\n"
        "            QPushButton:disabled {\n"
        "                background-color: #ccc; /* Color cuando el botón está deshabilitado */\n"
        "            }")
        self.button_cerrar.setObjectName("button_cerrar")
        #self.button_cerrar.clicked.connect(MainWindow.close)  # Conecta el botón a la función close()

        # Crea el botón de cancelar
        self.button_cancelar = QtWidgets.QPushButton(self.centralwidget)
        self.button_cancelar.setGeometry(QtCore.QRect(920, 605, 75, 31))
        self.button_cancelar.setText("Cancelar")
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

        self.button_modificar = QtWidgets.QPushButton(self.centralwidget)
        self.button_modificar.setGeometry(QtCore.QRect(739, 605, 75, 31))
        self.button_modificar.setStyleSheet("QPushButton {\n"
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
        self.button_modificar.clicked.connect(self.modificar_producto)


        self.button_crear = QtWidgets.QPushButton(self.centralwidget)
        self.button_crear.setGeometry(QtCore.QRect(650, 605, 75, 31))
        self.button_crear.setStyleSheet("QPushButton {\n"
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
        self.button_crear.setObjectName("button_crear")

        # Conectar el botón "Crear" a la función habilitar_codigo
        self.button_crear.clicked.connect(self.habilitar_codigo)

        self.button_delete = QtWidgets.QPushButton(self.centralwidget)
        self.button_delete.setGeometry(QtCore.QRect(830, 605, 75, 31))
        self.button_delete.setStyleSheet("QPushButton {\n"
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
        self.button_delete.clicked.connect(self.eliminar_producto)


        self.tab_widget.raise_()
        self.codigo_edit.raise_()
        self.codigo_label.raise_()
        self.descripcion_edit.raise_()
        self.marca_comboBox.raise_()
        self.marca_label.raise_()
        self.linea_comboBox.raise_()
        self.deposito_label.raise_()
        self.deposito_comboBox.raise_()
        self.linea_label.raise_()
        self.unidad_label.raise_()
        self.unidad_edit.raise_()
        self.paquete_label.raise_()
        self.paquete_edit.raise_()
        self.costo_moneda_local_groupBox.raise_()
        self.costo_moneda_referencial_groupBox.raise_()
        self.button_impuestos.raise_()
        self.button_cerrar.raise_()
        self.button_modificar.raise_()
        self.button_crear.raise_()
        self.button_delete.raise_()
        self.button_cancelar.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        self.precios_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Deshabilita los campos de entrada
        self.codigo_edit.setDisabled(True)
        self.descripcion_edit.setDisabled(True)
        self.unidad_edit.setDisabled(True)
        self.paquete_edit.setDisabled(True)
        self.costo_anterior_edit.setDisabled(True)
        self.costo_actual_edit.setDisabled(True)
        self.costo_promedio_edit.setDisabled(True)
        self.costo_reposicion_edit.setDisabled(True)
        self.moneda_referencial_edit.setDisabled(True)
        self.costo_actual_referencial_edit.setDisabled(True)
        self.utilidad_bs_edit.setDisabled(True)
        self.precio_sin_impuesto_bs_edit.setDisabled(True)
        self.impuesto_total_bs_edit.setDisabled(True)
        self.precio_total_bs_edit.setDisabled(True)
        self.lineEdit_17.setDisabled(True)
        self.utilidad_dolar_edit.setDisabled(True)
        self.precio_dolar_sin_impuesto_edit.setDisabled(True)
        self.precio_total_dolar_edit.setDisabled(True)
        self.utilidad_bs_edit_2.setDisabled(True)
        self.precio_sin_impuesto_bs_edit_2.setDisabled(True)
        self.impuesto_total_bs_edit_2.setDisabled(True)
        self.precio_total_bs_edit_2.setDisabled(True)
        self.lineEdit_18.setDisabled(True)
        self.utilidad_dolar_edit_2.setDisabled(True)
        self.precio_dolar_sin_impuesto_edit_2.setDisabled(True)
        self.precio_total_dolar_edit_2.setDisabled(True)
        self.utilidad_bs_edit_3.setDisabled(True)
        self.precio_sin_impuesto_bs_edit_3.setDisabled(True)
        self.impuesto_total_bs_edit_3.setDisabled(True)
        self.precio_total_bs_edit_3.setDisabled(True)
        self.lineEdit_19.setDisabled(True)
        self.utilidad_dolar_edit_3.setDisabled(True)
        self.precio_dolar_sin_impuesto_edit_3.setDisabled(True)
        self.precio_total_dolar_edit_3.setDisabled(True)
        self.peso_litro_edit.setDisabled(True)
        self.existencia_maxima_edit.setDisabled(True)
        self.existencia_minima_edit.setDisabled(True)
        self.codigo_barra_edit.setDisabled(True)
        self.moneda_listView.setDisabled(True)
        self.moneda_ref_listView.setDisabled(True)

        # Deshabilita los QComboBox
        self.marca_comboBox.setDisabled(True)
        self.linea_comboBox.setDisabled(True)
        self.deposito_comboBox.setDisabled(True)

        # Deshabilita los checkbox
        self.activo_checkBox.setDisabled(True)

        # Deshabilita los botones "Añadir" y "Borrar"
        self.button_impuestos.setDisabled(True)
        self.button_anadir.setDisabled(True)
        self.button_borrar.setDisabled(True)
        self.button_ultimas_transacciones.setDisabled(True)
        self.button_modificar.setDisabled(True)
        self.button_delete.setDisabled(True)
        self.button_cancelar.setDisabled(True)

        # Agrega estas líneas al final del método setupUi
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_barra_estado)
        self.timer.start(1000)  # Actualiza cada segundo

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Crear Productos"))
        MainWindow.setWindowIcon(QIcon('icono.png'))  # Agrega el icono a la ventana
        self.codigo_label.setText(_translate("MainWindow", "Código"))
        self.marca_label.setText(_translate("MainWindow", "Marca"))
        self.linea_label.setText(_translate("MainWindow", "Linea de Productos"))
        self.unidad_label.setText(_translate("MainWindow", "Unidad"))
        self.paquete_label.setText(_translate("MainWindow", "Paquete"))
        self.costo_moneda_local_groupBox.setTitle(_translate("MainWindow", "Costo Moneda Local"))
        self.costo_anterior_label.setText(_translate("MainWindow", "Costo Anterior"))
        self.costo_actual_label.setText(_translate("MainWindow", "Costo Actual"))
        self.costo_promedio_label.setText(_translate("MainWindow", "Costo Promedio"))
        self.costo_reposicion_label.setText(_translate("MainWindow", "Costo Reposición"))
        self.costo_moneda_referencial_groupBox.setTitle(_translate("MainWindow", "Costo Moneda Referencial"))
        self.moneda_referencial_label.setText(_translate("MainWindow", "Moneda Referencial"))
        self.costo_actual_referencial_label.setText(_translate("MainWindow", "Costo Actual"))
        self.utilidad_bs_label.setText(_translate("MainWindow", "Utilidad"))
        self.precio_sin_impuesto_bs_label.setText(_translate("MainWindow", "Precio sin Impuesto"))
        self.impuesto_total_bs_label.setText(_translate("MainWindow", "Impuesto Total"))
        self.precio_total_bs_label.setText(_translate("MainWindow", "Precio Total"))
        self.bs_label.setText(_translate("MainWindow", "Bs."))
        self.precio_dolar_sin_impuesto_label.setText(_translate("MainWindow", "Precio sin Impuesto"))
        self.precio_total_dolar_label.setText(_translate("MainWindow", "Precio Total"))
        self.utilidad_dolar_label.setText(_translate("MainWindow", "Utilidad"))
        self.precios_tab.setTabText(self.precios_tab.indexOf(self.tab_3), _translate("MainWindow", "Precio 1"))
        self.precio_sin_impuesto_bs_label_2.setText(_translate("MainWindow", "Precio sin Impuesto"))
        self.precio_total_bs_label_2.setText(_translate("MainWindow", "Precio Total"))
        self.bs_label_2.setText(_translate("MainWindow", "Bs."))
        self.precio_dolar_sin_impuesto_label_2.setText(_translate("MainWindow", "Precio sin Impuesto"))
        self.utilidad_bs_label_2.setText(_translate("MainWindow", "Utilidad"))
        self.impuesto_total_bs_label_2.setText(_translate("MainWindow", "Impuesto Total"))
        self.precio_total_dolar_label_2.setText(_translate("MainWindow", "Precio Total"))
        self.utilidad_dolar_label_2.setText(_translate("MainWindow", "Utilidad"))
        self.precios_tab.setTabText(self.precios_tab.indexOf(self.tab), _translate("MainWindow", "Precio 2"))
        self.precio_sin_impuesto_bs_label_3.setText(_translate("MainWindow", "Precio sin Impuesto"))
        self.utilidad_dolar_label_3.setText(_translate("MainWindow", "Utilidad"))
        self.precio_total_dolar_label_3.setText(_translate("MainWindow", "Precio Total"))
        self.precio_dolar_sin_impuesto_label_3.setText(_translate("MainWindow", "Precio sin Impuesto"))
        self.precio_total_bs_label_3.setText(_translate("MainWindow", "Precio Total"))
        self.impuesto_total_bs_label_3.setText(_translate("MainWindow", "Impuesto Total"))
        self.utilidad_bs_label_3.setText(_translate("MainWindow", "Utilidad"))
        self.bs_label_3.setText(_translate("MainWindow", "Bs."))
        self.precios_tab.setTabText(self.precios_tab.indexOf(self.tab_2), _translate("MainWindow", "Precio 3"))
        self.activo_checkBox.setText(_translate("MainWindow", "Activo"))
        item = self.table_productos.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Código"))
        item = self.table_productos.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Descripción"))
        item = self.table_productos.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Marca"))
        item = self.table_productos.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Existencia"))
        item = self.table_productos.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Precio Bs."))
        item = self.table_productos.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Precio $"))
        self.peso_litro_label.setText(_translate("MainWindow", "Peso/Litro"))
        self.existencia_maxima_label.setText(_translate("MainWindow", "Exist. Maxima"))
        self.existencia_minima_label.setText(_translate("MainWindow", "Exist. Minima"))
        self.deposito_label.setText(_translate("MainWindow", "Depósito"))
        self.codigo_barra_label.setText(_translate("MainWindow", "Referencia"))
        self.imagen_producto_label.setText(_translate("MainWindow", "Imagen de Producto"))
        self.button_anadir.setText(_translate("MainWindow", "Añadir"))
        self.button_borrar.setText(_translate("MainWindow", "Borrar"))
        self.button_ultimas_transacciones.setText(_translate("MainWindow", "Ultimas Transacciones"))
        self.button_etiqueta.setText(_translate("MainWindow", "Generar Etiqueta"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_6), _translate("MainWindow", "Ficha de Producto"))
        self.button_importar.setText(_translate("MainWindow", "Importar"))
        self.button_exportar.setText(_translate("MainWindow", "Exportar"))
        self.button_impuestos.setText(_translate("MainWindow", "Impuestos"))
        self.button_cerrar.setText(_translate("MainWindow", "Cerrar"))
        self.button_modificar.setText(_translate("MainWindow", "Modificar"))
        self.button_crear.setText(_translate("MainWindow", "Crear"))
        self.button_delete.setText(_translate("MainWindow", "Eliminar"))
        self.button_cancelar.setText(_translate("MainWindow", "Cancelar"))

    def configurar_checkboxes(self):
        if self.es_nuevo_producto:
            # Establecer el checkbox de impuesto como seleccionado por defecto
            self.iva_check.setChecked(True)  # Por ejemplo, seleccionando IVA
        else:
            # Aquí puedes cargar el estado de los checkboxes para un producto existente
            self.cargar_estado_checkboxes()
    
    def abrir_seleccion_impuestos(self):
        impuestos_seleccionados = self.productos_impuestos.get(self.codigo_edit.text(), {})
        
        self.ventana = SeleccionImpuestos(impuestos_predeterminados=impuestos_seleccionados, es_nuevo_producto=self.es_nuevo_producto)
        self.ventana.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ventana.exec_()  # Cambia a exec_() para esperar la respuesta

        # Obtener los impuestos seleccionados
        self.impuestos_seleccionados = self.ventana.obtener_impuestos_seleccionados()
        print(self.impuestos_seleccionados)  # Aquí puedes ver qué impuestos fueron seleccionados

    def habilitar_codigo(self):
        # Habilita solo el campo de código
        self.codigo_edit.setDisabled(False)
        self.codigo_edit.clear()
        self.table_productos.setDisabled(True)
        self.button_cancelar.setDisabled(False)

    def verificar_codigo(self):
        codigo = self.codigo_edit.text().strip()

        # Verifica si el campo está vacío
        if not codigo:
            # Cambia el color de fondo del campo a un color llamativo (por ejemplo, rojo)
            self.codigo_edit.setStyleSheet("border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                background-color: yellow;")
            
            QtWidgets.QMessageBox.warning(self, "Código vacío", "El campo de código no puede estar vacío. Por favor, ingrese un código.")
            return  # Salir de la función si el campo está vacío
        
        # Si el campo no está vacío, restablece el color de fondo a su estado original
        self.codigo_edit.setStyleSheet("border: 1px solid #6b797e; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n")
        
        # Verifica si el código ya existe en la base de datos
        if self.codigo_existe(codigo):
            QtWidgets.QMessageBox.warning(self, "Código existente", "El código ya existe. Por favor, ingrese un código nuevo.")
        else:
            self.habilitar_campos()  # Si el código no existe, habilita los demás campos

    def codigo_existe(self, codigo):
        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        
        # Ejecutar la consulta para verificar si el código existe
        cursor.execute("SELECT COUNT(*) FROM productos_inventario WHERE codigo = ?", (codigo,))
        resultado = cursor.fetchone()
        
        # Cerrar la conexión
        conn.close()
        
        # Si el resultado es mayor que 0, el código existe
        return resultado[0] > 0

    def convertir_a_mayusculas(self, texto):
        # Convierte el texto a mayúsculas
        self.codigo_edit.setText(texto.upper())
        # Mueve el cursor al final del texto
        self.codigo_edit.setCursorPosition(len(texto))

    def importar_inventario(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Importar Inventario", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            df = pd.read_excel(fileName)  # Cargar el archivo Excel
            # Aquí deberías agregar el código para guardar los datos del DataFrame en tu base de datos
            for index, row in df.iterrows():
                # Supongamos que tienes una función para guardar un producto en la base de datos
                self.guardar_producto_en_db(row)

    def exportar_inventario(self):
        # Aquí deberías obtener los datos de tu base de datos y convertirlos a un DataFrame
        df = self.obtener_inventario_de_db()  # Implementa esta función para obtener los datos
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Exportar Inventario", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            df.to_excel(fileName, index=False)  # Guarda el DataFrame como un archivo Excel

    def obtener_inventario_de_db(self):
        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Preparar la consulta SQL para seleccionar todos los productos
        query = "SELECT * FROM productos_inventario"  # Ajusta esto según tus necesidades

        # Ejecutar la consulta
        cursor.execute(query)

        # Obtener todos los resultados
        rows = cursor.fetchall()

        # Obtener los nombres de las columnas
        column_names = [description[0] for description in cursor.description]

        # Cerrar la conexión a la base de datos
        conn.close()

        # Crear un DataFrame de pandas a partir de los resultados
        df = pd.DataFrame(rows, columns=column_names)

        return df

    def filtrar_productos(self):
        texto_busqueda = self.buscar_producto_edit.text().lower()
        for fila in range(self.table_productos.rowCount()):
            # Obtener el texto de cada celda
            codigo = self.table_productos.item(fila, 0).text().lower()
            descripcion = self.table_productos.item(fila, 1).text().lower()

            # Comprobar si el texto de búsqueda está en el código o descripción
            if texto_busqueda in codigo or texto_busqueda in descripcion:
                self.table_productos.showRow(fila)  # Mostrar la fila si coincide
            else:
                self.table_productos.hideRow(fila)  # Ocultar la fila si no coincide

    def generar_etiqueta(self):
        # Obtener el índice de la fila seleccionada
        fila_seleccionada = self.table_productos.currentRow()
        
        # Obtener información del producto seleccionado
        codigo_producto = self.table_productos.item(fila_seleccionada, 0).text()
        nombre_producto = self.table_productos.item(fila_seleccionada, 1).text()

        # Obtener el código de barras desde la base de datos
        codigo_barras = self.obtener_codigo_barras(codigo_producto)
        
        if codigo_barras:
            # Generar el código de barras y guardarlo
            self.generar_codigo_barras(codigo_barras)

            # Crear la imagen de la etiqueta
            etiqueta_ancho = 300
            etiqueta_alto = 200
            imagen = Image.new('RGB', (etiqueta_ancho, etiqueta_alto), color='white')
            d = ImageDraw.Draw(imagen)

            # Definir la fuente (puedes cambiar la fuente y tamaño)
            fuente = ImageFont.load_default()

            # Calcular el tamaño del texto usando textbbox
            bbox_nombre = d.textbbox((0, 0), nombre_producto, font=fuente)
            bbox_codigo = d.textbbox((0, 0), codigo_producto, font=fuente)

            ancho_nombre = bbox_nombre[2] - bbox_nombre[0]  # bbox[2] es el ancho derecho, bbox[0] es el ancho izquierdo
            alto_nombre = bbox_nombre[3] - bbox_nombre[1]   # bbox[3] es el alto inferior, bbox[1] es el alto superior

            ancho_codigo = bbox_codigo[2] - bbox_codigo[0]
            alto_codigo = bbox_codigo[3] - bbox_codigo[1]

            # Calcular las posiciones centradas
            pos_nombre = ((etiqueta_ancho - ancho_nombre) // 2, 10)  # 10 píxeles desde la parte superior
            pos_codigo = ((etiqueta_ancho - ancho_codigo) // 2, pos_nombre[1] + alto_nombre + 2)  # 10 píxeles entre textos

            # Añadir texto a la imagen
            d.text(pos_nombre, nombre_producto, fill=(0, 0, 0), font=fuente)
            d.text(pos_codigo, codigo_producto, fill=(0, 0, 0), font=fuente)

            # Cargar el código de barras y añadirlo a la etiqueta
            codigo_barras_imagen = f'codigo_barra_{codigo_barras}.png'
            # Obtener la ruta completa del archivo
            directory = os.path.dirname(os.path.abspath(__file__))
            codigo_barras_path = os.path.join(directory, codigo_barras_imagen)

            # Verificar si el archivo existe antes de abrirlo
            if os.path.exists(codigo_barras_path):
                try:
                    codigo_barras_pixmap = Image.open(codigo_barras_path)
                    
                    # Definir las dimensiones máximas
                    max_ancho_codigo = 300
                    max_alto_codigo = 150

                    # Mantener la relación de aspecto
                    ancho_original, alto_original = codigo_barras_pixmap.size
                    ratio = ancho_original / alto_original

                    if ancho_original > max_ancho_codigo:
                        # Redimensionar por ancho
                        nuevo_ancho = max_ancho_codigo
                        nuevo_alto = int(nuevo_ancho / ratio)
                    else:
                        nuevo_ancho = ancho_original
                        nuevo_alto = alto_original

                    if nuevo_alto > max_alto_codigo:
                        # Redimensionar por altura
                        nuevo_alto = max_alto_codigo
                        nuevo_ancho = int(nuevo_alto * ratio)

                    # Redimensionar la imagen del código de barras
                    codigo_barras_pixmap = codigo_barras_pixmap.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

                    # Calcular la posición centrada para el código de barras
                    pos_codigo_barras = ((etiqueta_ancho - codigo_barras_pixmap.width) // 2, etiqueta_alto - codigo_barras_pixmap.height - 10)  # 10 píxeles desde la parte inferior

                    # Pegar la imagen del código de barras en la etiqueta
                    imagen.paste(codigo_barras_pixmap, pos_codigo_barras)

                    imagen.paste(codigo_barras_pixmap, pos_codigo_barras)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo de código de barras: {e}")
                    return
            else:
                QMessageBox.warning(self, "Error", f"No se encontró el archivo de código de barras: {codigo_barras_path}")
                return

            # Guardar la imagen de la etiqueta
            etiqueta_path = "etiqueta.png"
            imagen.save(etiqueta_path)

            # Abrir la imagen con el visualizador de imágenes predeterminado del sistema
            if os.name == 'nt':  # Windows
                os.startfile(etiqueta_path)
            elif os.name == 'posix':  # Linux o Mac
                subprocess.run(['open', etiqueta_path])  # Para Mac
                # subprocess.run(['xdg-open', etiqueta_path])  # Para Linux
        else:
            QMessageBox.warning(self, "Error", "No se encontró el código de barras para el producto seleccionado.")

    def obtener_codigo_barras(self, codigo_producto):
        # Conectar a la base de datos (ajusta la ruta según tu configuración)
        conexion = sqlite3.connect('Usuarios.db')
        cursor = conexion.cursor()

        # Consulta para obtener el código de barras
        cursor.execute("SELECT codigo_barra FROM productos_inventario WHERE codigo = ?", (codigo_producto,))
        resultado = cursor.fetchone()

        conexion.close()

        if resultado:
            return resultado[0]  # Retorna el código de barras
        return None  # Si no se encuentra, retorna None
    
    def generar_codigo_barras(self, codigo_barras):
        # Generar el código de barras
        codigo_barras_obj = barcode.get('code128', codigo_barras, writer=ImageWriter())
        directory = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(directory, f'codigo_barra_{codigo_barras}')
        codigo_barras_obj.save(filename)

        print(f"Código de barras guardado en: {filename}")

    def toggle_generar_etiqueta_button(self):
        # Habilitar el botón si hay una fila seleccionada
        self.button_etiqueta.setEnabled(len(self.table_productos.selectedItems()) > 0)

    def mostrar_imagen_producto(self, seleccionada, deseleccionada):
        # Limpiar la escena primero
        self.imagen_scene.clear()
        
        # Solo proceder si hay una selección válida
        if not seleccionada:
            self.imagen_producto_graphicsView.setScene(self.imagen_scene)
            return

        indice = self.table_productos.currentRow()
        if indice == -1:
            return

        # Obtener el código del producto
        codigo_item = self.table_productos.item(indice, 0)
        if not codigo_item:
            return

        codigo = codigo_item.text()
        imagen_ruta = f"imagen_productos/producto_{codigo}.png"

        # Verificar si el archivo de imagen existe
        if not os.path.exists(imagen_ruta):
            return

        # Cargar y escalar la imagen
        pixmap = QPixmap(imagen_ruta)
        if pixmap.isNull():
            return

        # Escalar manteniendo relación de aspecto
        scaled_pixmap = pixmap.scaled(
            self.imagen_producto_graphicsView.width() - 10,
            self.imagen_producto_graphicsView.height() - 10,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # Crear y mostrar el item
        item = QGraphicsPixmapItem(scaled_pixmap)
        self.imagen_scene.addItem(item)
        self.imagen_producto_graphicsView.setScene(self.imagen_scene)
        
        # Ajustar la vista
        self.imagen_producto_graphicsView.fitInView(item, Qt.KeepAspectRatio)

    def seleccionar_imagen(self):
        imagen_ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imagenes (*.png *.jpg *.jpeg)")
        if imagen_ruta:
            self.imagen_ruta = imagen_ruta
            pixmap = QPixmap(imagen_ruta)

            if pixmap.isNull():
                QMessageBox.warning(self, "Error", "No se pudo cargar la imagen.")
                return
            
            # Escalar la imagen manteniendo la relación de aspecto para que quepa en el QGraphicsView
            scaled_pixmap = pixmap.scaled(
                self.imagen_producto_graphicsView.width() - 10,  # -10 para margen interno
                self.imagen_producto_graphicsView.height() - 10,
                Qt.KeepAspectRatio,  # Mantener relación de aspecto
                Qt.SmoothTransformation  # Suavizado para mejor calidad
            )
            
            item = QGraphicsPixmapItem(scaled_pixmap)
            self.imagen_scene.clear()
            self.imagen_scene.addItem(item)
            self.imagen_producto_graphicsView.setScene(self.imagen_scene)
            
            # Configurar el rectángulo de la escena correctamente
            self.imagen_producto_graphicsView.setSceneRect(0, 0, 
                                                        scaled_pixmap.width(), 
                                                        scaled_pixmap.height())
            self.imagen_producto_graphicsView.fitInView(item, Qt.KeepAspectRatio)

    def borrar_imagen(self):
        # Verificar si hay un producto seleccionado
        indice = self.table_productos.currentRow()
        if indice == -1:
            QMessageBox.warning(self, "Advertencia", "No hay ningún producto seleccionado")
            return

        # Obtener el código del producto
        codigo_item = self.table_productos.item(indice, 0)
        if not codigo_item:
            return

        codigo = codigo_item.text()
        imagen_ruta = f"imagen_productos/producto_{codigo}.png"

        # Preguntar confirmación al usuario
        respuesta = QMessageBox.question(
            self,
            "Confirmar borrado",
            "¿Estás seguro de que quieres eliminar la imagen de este producto?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            # 1. Eliminar el archivo de imagen si existe
            if os.path.exists(imagen_ruta):
                try:
                    os.remove(imagen_ruta)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar la imagen: {str(e)}")
                    return

            # 2. Limpiar la vista gráfica
            self.imagen_scene.clear()
            self.imagen_producto_graphicsView.setScene(self.imagen_scene)
            QMessageBox.information(self, "Éxito", "La imagen ha sido eliminada correctamente")

    def cancelar(self):
        # Limpia los campos de entrada
        self.codigo_edit.clear()
        self.codigo_barra_edit.clear()
        self.descripcion_edit.clear()
        self.unidad_edit.clear()
        self.existencia_minima_edit.clear()
        self.paquete_edit.clear()
        self.costo_anterior_edit.clear()
        self.costo_actual_edit.clear()
        self.costo_promedio_edit.clear()
        self.costo_reposicion_edit.clear()
        self.costo_actual_referencial_edit.clear()

        self.utilidad_bs_edit.setText("0%")
        self.utilidad_bs_edit_2.setText("0%")
        self.utilidad_bs_edit_3.setText("0%")
        self.precio_sin_impuesto_bs_edit.setText("0.00")
        self.precio_sin_impuesto_bs_edit_2.setText("0.00")
        self.precio_sin_impuesto_bs_edit_3.setText("0.00")
        self.impuesto_total_bs_edit.setText("0.00")
        self.impuesto_total_bs_edit_2.setText("0.00")
        self.impuesto_total_bs_edit_3.setText("0.00")
        self.precio_total_bs_edit.setText("0.00")
        self.precio_total_bs_edit_2.setText("0.00")
        self.precio_total_bs_edit_3.setText("0.00")
        self.lineEdit_17.setText("0.00")
        self.lineEdit_18.setText("0.00")
        self.lineEdit_19.setText("0.00")
        self.utilidad_dolar_edit.setText("0%")
        self.utilidad_dolar_edit_2.setText("0%")
        self.utilidad_dolar_edit_3.setText("0%")
        self.precio_dolar_sin_impuesto_edit.setText("0.00")
        self.precio_dolar_sin_impuesto_edit_2.setText("0.00")
        self.precio_dolar_sin_impuesto_edit_3.setText("0.00")
        self.precio_total_dolar_edit.setText("0.00")
        self.precio_total_dolar_edit_2.setText("0.00")
        self.precio_total_dolar_edit_3.setText("0.00")

        # Limpia los combobox
        self.marca_comboBox.setCurrentIndex(0)
        self.linea_comboBox.setCurrentIndex(0)

        # Limpia la imagen
        self.imagen_scene.clear()
        self.imagen_producto_graphicsView.setScene(self.imagen_scene)

        # Deshabilita los campos, combobox
        self.codigo_edit.setDisabled(True)
        self.descripcion_edit.setDisabled(True)
        self.unidad_edit.setDisabled(True)
        self.peso_litro_edit.setDisabled(True)
        self.codigo_barra_edit.setDisabled(True)
        self.existencia_minima_edit.setDisabled(True)
        self.existencia_maxima_edit.setDisabled(True)
        self.lineEdit_17.setDisabled(True)
        self.lineEdit_18.setDisabled(True)
        self.lineEdit_19.setDisabled(True)
        self.paquete_edit.setDisabled(True)
        self.costo_anterior_edit.setDisabled(True)
        self.costo_actual_edit.setDisabled(True)
        self.costo_promedio_edit.setDisabled(True)
        self.costo_reposicion_edit.setDisabled(True)
        self.costo_actual_referencial_edit.setDisabled(True)
        self.utilidad_bs_edit.setDisabled(True)
        self.utilidad_bs_edit_2.setDisabled(True)
        self.utilidad_bs_edit_3.setDisabled(True)
        self.precio_sin_impuesto_bs_edit.setDisabled(True)
        self.precio_sin_impuesto_bs_edit_2.setDisabled(True)
        self.precio_sin_impuesto_bs_edit_3.setDisabled(True)
        self.impuesto_total_bs_edit.setDisabled(True)
        self.impuesto_total_bs_edit_2.setDisabled(True)
        self.impuesto_total_bs_edit_3.setDisabled(True)
        self.precio_total_bs_edit.setDisabled(True)
        self.precio_total_bs_edit_2.setDisabled(True)
        self.precio_total_bs_edit_3.setDisabled(True)
        self.utilidad_dolar_edit.setDisabled(True)
        self.utilidad_dolar_edit_2.setDisabled(True)
        self.utilidad_dolar_edit_3.setDisabled(True)
        self.precio_dolar_sin_impuesto_edit.setDisabled(True)
        self.precio_dolar_sin_impuesto_edit_2.setDisabled(True)
        self.precio_dolar_sin_impuesto_edit_3.setDisabled(True)
        self.precio_total_dolar_edit.setDisabled(True)
        self.precio_total_dolar_edit_2.setDisabled(True)
        self.precio_total_dolar_edit_3.setDisabled(True)

        # Combobox y checkbox
        self.marca_comboBox.setDisabled(True)
        self.linea_comboBox.setDisabled(True)
        self.deposito_comboBox.setDisabled(True)
        self.activo_checkBox.setDisabled(True)
        self.button_impuestos.setDisabled(True)

        # Limpia los Botones
        self.button_anadir.setDisabled(True)
        self.button_borrar.setDisabled(True)

        self.table_productos.setDisabled(False)
        
        self.button_modificar.setText("Modificar")
        self.button_modificar.clicked.disconnect()
        self.button_modificar.clicked.connect(self.modificar_producto)

        # Cambia el texto del botón de guardar a "Crear"
        self.button_crear.setText("Crear")
        self.button_crear.clicked.disconnect()
        self.button_crear.clicked.connect(self.habilitar_codigo)

        self.button_cancelar.setDisabled(True)
        self.costo_actual_calculado = False

        # Refrescar la tabla para mostrar los cambios
        self.table_productos.setRowCount(0)  # Limpiar la tabla
        self.cargar_productos_en_tabla()  # Cargar los productos nuevamente

    def habilitar_eliminar(self):
        # Obtén la selección actual
        selection = self.table_productos.selectionModel().selection()
        
        # Si hay alguna fila seleccionada, habilita los botones
        if selection.count() > 0:
            self.button_delete.setDisabled(False)
            self.button_modificar.setDisabled(False)
            self.button_crear.setDisabled(True)
            self.button_cancelar.setDisabled(False)
            self.button_ultimas_transacciones.setDisabled(False)
        # Si no hay ninguna fila seleccionada, deshabilita los botones
        else:
            self.button_delete.setDisabled(True)
            self.button_modificar.setDisabled(True)
            self.button_crear.setDisabled(False)
            self.button_cancelar.setDisabled(True)
            self.button_ultimas_transacciones.setDisabled(True)

    def on_return_pressed(self):
        # Obtener el texto actual
        current_text = self.utilidad_dolar_edit.text().strip()
        if current_text and not current_text.endswith('%'):
            # Agregar el símbolo de porcentaje al final
            self.utilidad_dolar_edit.setText(current_text + '%')

        current_text = self.utilidad_dolar_edit_2.text().strip()
        if current_text and not current_text.endswith('%'):
            # Agregar el símbolo de porcentaje al final
            self.utilidad_dolar_edit_2.setText(current_text + '%')

        current_text = self.utilidad_dolar_edit_3.text().strip()
        if current_text and not current_text.endswith('%'):
            # Agregar el símbolo de porcentaje al final
            self.utilidad_dolar_edit_3.setText(current_text + '%')
        
        # Llamar a la función para calcular la utilidad
        self.calcular_utilidad_dolar()

    def on_return_pressed_2(self):
        # Obtener el texto actual
        current_text = self.utilidad_dolar_edit_2.text().strip()
        if current_text and not current_text.endswith('%'):
            # Agregar el símbolo de porcentaje al final
            self.utilidad_dolar_edit_2.setText(current_text + '%')
        
        # Llamar a la función para calcular la utilidad
        self.calcular_utilidad_dolar_2()

    def on_return_pressed_3(self):
        # Obtener el texto actual
        current_text = self.utilidad_dolar_edit_3.text().strip()
        if current_text and not current_text.endswith('%'):
            # Agregar el símbolo de porcentaje al final
            self.utilidad_dolar_edit_3.setText(current_text + '%')
        
        # Llamar a la función para calcular la utilidad
        self.calcular_utilidad_dolar_3()

    def calcular_utilidad_dolar(self):
        # Obtener el costo actual y el costo actual referencial
        costo_actual = float(self.costo_actual_edit.text() or "0")
        costo_actual_referencial = float(self.costo_actual_referencial_edit.text() or "0")

        # Obtener el porcentaje de utilidad ingresado
        utilidad_dolar = self.utilidad_dolar_edit.text().replace("%", "").strip()
        if utilidad_dolar == "" or not utilidad_dolar.replace('.', '', 1).isdigit():
            return  # Si no es un número válido, no hacemos nada

        utilidad_dolar = round(float(utilidad_dolar) / 100, 6)  # Convertir a decimal

        # Calcular el precio sin impuesto
        precio_sin_impuesto_dolar = costo_actual_referencial * (1 + utilidad_dolar)

        # Calcular el impuesto si el IVA está seleccionado
        if self.impuestos_seleccionados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False):
            tasa_impuesto = self.obtener_tasa_impuesto()
            impuesto_dolar = precio_sin_impuesto_dolar * tasa_impuesto
        else:
            impuesto_dolar = 0.0

        # Calcular el precio total
        precio_total_dolar = precio_sin_impuesto_dolar + impuesto_dolar

        # Actualizar los campos correspondientes
        self.precio_dolar_sin_impuesto_edit.setText(str(round(precio_sin_impuesto_dolar, 4)))
        self.precio_total_dolar_edit.setText(str(round(precio_total_dolar, 4)))

    def calcular_utilidad_dolar_2(self):
        # Obtener el costo actual y el costo actual referencial
        costo_actual = float(self.costo_actual_edit.text() or "0")
        costo_actual_referencial = float(self.costo_actual_referencial_edit.text() or "0")

        # Obtener el porcentaje de utilidad ingresado
        utilidad_dolar = self.utilidad_dolar_edit_2.text().replace("%", "").strip()
        if utilidad_dolar == "" or not utilidad_dolar.replace('.', '', 1).isdigit():
            return  # Si no es un número válido, no hacemos nada

        utilidad_dolar = round(float(utilidad_dolar) / 100, 6)  # Convertir a decimal

        # Calcular el precio sin impuesto
        precio_sin_impuesto_dolar = costo_actual_referencial * (1 + utilidad_dolar)

        # Calcular el impuesto si el IVA está seleccionado
        if self.impuestos_seleccionados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False):
            tasa_impuesto = self.obtener_tasa_impuesto()
            impuesto_dolar = precio_sin_impuesto_dolar * tasa_impuesto
        else:
            impuesto_dolar = 0.0

        # Calcular el precio total
        precio_total_dolar = precio_sin_impuesto_dolar + impuesto_dolar

        # Actualizar los campos correspondientes
        self.precio_dolar_sin_impuesto_edit_2.setText(str(round(precio_sin_impuesto_dolar, 4)))
        self.precio_total_dolar_edit_2.setText(str(round(precio_total_dolar, 4)))

    def calcular_utilidad_dolar_3(self):
        # Obtener el costo actual y el costo actual referencial
        costo_actual = float(self.costo_actual_edit.text() or "0")
        costo_actual_referencial = float(self.costo_actual_referencial_edit.text() or "0")

        # Obtener el porcentaje de utilidad ingresado
        utilidad_dolar = self.utilidad_dolar_edit_3.text().replace("%", "").strip()
        if utilidad_dolar == "" or not utilidad_dolar.replace('.', '', 1).isdigit():
            return  # Si no es un número válido, no hacemos nada

        utilidad_dolar = round(float(utilidad_dolar) / 100, 6)  # Convertir a decimal

        # Calcular el precio sin impuesto
        precio_sin_impuesto_dolar = costo_actual_referencial * (1 + utilidad_dolar)

        # Calcular el impuesto si el IVA está seleccionado
        if self.impuestos_seleccionados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False):
            tasa_impuesto = self.obtener_tasa_impuesto()
            impuesto_dolar = precio_sin_impuesto_dolar * tasa_impuesto
        else:
            impuesto_dolar = 0.0

        # Calcular el precio total
        precio_total_dolar = precio_sin_impuesto_dolar + impuesto_dolar

        # Actualizar los campos correspondientes
        self.precio_dolar_sin_impuesto_edit_3.setText(str(round(precio_sin_impuesto_dolar, 4)))
        self.precio_total_dolar_edit_3.setText(str(round(precio_total_dolar, 4)))

    def calcular_utilidad_y_impuesto(self):
        # Obtener el costo actual y el costo actual referencial
        costo_actual_referencial = float(self.costo_actual_referencial_edit.text() or "0")

        # Obtener el precio total ingresado
        precio_total_dolar = self.precio_total_dolar_edit.text()
        if precio_total_dolar == "" or not precio_total_dolar.replace('.', '', 1).isdigit():
            return  # Si no es un número válido, no hacemos nada

        precio_total_dolar = float(precio_total_dolar)

        # Calcular el impuesto si el IVA está seleccionado
        if self.impuestos_seleccionados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False):
            tasa_impuesto = self.obtener_tasa_impuesto()
            precio_sin_impuesto_dolar = precio_total_dolar / (1 + tasa_impuesto)
        else:
            precio_sin_impuesto_dolar = precio_total_dolar

        # Verificar que el costo actual referencial no sea cero antes de calcular la utilidad
        if costo_actual_referencial == 0:
            # Manejar el caso de división por cero
            self.utilidad_dolar_edit.setText("0%")  # O cualquier otro manejo que desees
            return
        
        # Calcular la utilidad en base al costo actual referencial
        moneda_referencial = float(self.moneda_referencial_edit.text() or "0")
        precio_bs_sin_impuesto = float(self.precio_sin_impuesto_bs_edit.text() or "0")
        utilidad_dolar = round(
            (precio_sin_impuesto_dolar - costo_actual_referencial) / costo_actual_referencial,
            6  # Redondear a 4 decimales
        )
        precio_bs_sin_impuesto = precio_sin_impuesto_dolar * moneda_referencial
        utilidad_bs_monto = (precio_sin_impuesto_dolar - costo_actual_referencial) * moneda_referencial
        
        if self.impuestos_seleccionados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False):
            tasa_impuesto = self.obtener_tasa_impuesto()
            impuesto_bs = precio_bs_sin_impuesto * tasa_impuesto
        else:
            impuesto_bs = 0.00

        precio_total_bs = precio_bs_sin_impuesto + impuesto_bs

        # Actualizar los campos correspondientes
        self.precio_dolar_sin_impuesto_edit.setText(str(round(precio_sin_impuesto_dolar, 4)))
        self.utilidad_dolar_edit.setText(str(round(utilidad_dolar * 100, 4)) + "%")
        self.utilidad_bs_edit.setText(str(round(utilidad_dolar * 100, 4)) + "%")
        self.lineEdit_17.setText(str(round(utilidad_bs_monto, 4)))
        self.precio_sin_impuesto_bs_edit.setText(str(round((precio_bs_sin_impuesto), 2)))
        self.impuesto_total_bs_edit.setText(str(round((impuesto_bs), 2)))
        self.precio_total_bs_edit.setText(str(round((precio_total_bs), 2)))

    def calcular_utilidad_y_impuesto_2(self):
        # Obtener el costo actual y el costo actual referencial
        costo_actual_referencial = float(self.costo_actual_referencial_edit.text() or "0")

        # Obtener el precio total ingresado
        precio_total_dolar = self.precio_total_dolar_edit_2.text()
        if precio_total_dolar == "" or not precio_total_dolar.replace('.', '', 1).isdigit():
            return  # Si no es un número válido, no hacemos nada

        precio_total_dolar = float(precio_total_dolar)

        # Calcular el impuesto si el IVA está seleccionado
        if self.impuestos_seleccionados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False):
            tasa_impuesto = self.obtener_tasa_impuesto()
            # Descomponer el precio total en precio sin impuesto y impuesto
            precio_sin_impuesto_dolar = precio_total_dolar / (1 + tasa_impuesto)
        else:
            precio_sin_impuesto_dolar = precio_total_dolar

        # Verificar que el costo actual referencial no sea cero antes de calcular la utilidad
        if costo_actual_referencial == 0:
            # Manejar el caso de división por cero
            self.utilidad_dolar_edit.setText("0%")  # O cualquier otro manejo que desees
            return
        
        # Calcular la utilidad en base al costo actual referencial
        moneda_referencial = float(self.moneda_referencial_edit.text() or "0")
        precio_bs_sin_impuesto = float(self.precio_sin_impuesto_bs_edit.text() or "0")
        utilidad_dolar = round(
            (precio_sin_impuesto_dolar - costo_actual_referencial) / costo_actual_referencial,
            6  # Redondear a 4 decimales
        )
        precio_bs_sin_impuesto = precio_sin_impuesto_dolar * moneda_referencial
        utilidad_bs_monto = (precio_sin_impuesto_dolar - costo_actual_referencial) * moneda_referencial
        
        if self.impuestos_seleccionados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False):
            tasa_impuesto = self.obtener_tasa_impuesto()
            # Descomponer el precio total en precio sin impuesto y impuesto
            impuesto_bs = precio_bs_sin_impuesto * tasa_impuesto
        else:
            impuesto_bs = 0.00

        precio_total_bs = precio_bs_sin_impuesto + impuesto_bs

        # Actualizar los campos correspondientes
        self.precio_dolar_sin_impuesto_edit_2.setText(str(round(precio_sin_impuesto_dolar, 4)))
        self.utilidad_dolar_edit_2.setText(str(round(utilidad_dolar * 100, 4)) + "%")
        self.utilidad_bs_edit_2.setText(str(round(utilidad_dolar * 100, 4)) + "%")
        self.lineEdit_18.setText(str(round(utilidad_bs_monto, 4)))
        self.precio_sin_impuesto_bs_edit_2.setText(str(round((precio_bs_sin_impuesto), 2)))
        self.impuesto_total_bs_edit_2.setText(str(round((impuesto_bs), 2)))
        self.precio_total_bs_edit_2.setText(str(round((precio_total_bs), 2)))

    def calcular_utilidad_y_impuesto_3(self):
        # Obtener el costo actual y el costo actual referencial
        costo_actual = float(self.costo_actual_edit.text() or "0")
        costo_actual_referencial = float(self.costo_actual_referencial_edit.text() or "0")

        # Obtener el precio total ingresado
        precio_total_dolar = self.precio_total_dolar_edit_3.text()
        if precio_total_dolar == "" or not precio_total_dolar.replace('.', '', 1).isdigit():
            return  # Si no es un número válido, no hacemos nada

        precio_total_dolar = float(precio_total_dolar)

        # Calcular el impuesto si el IVA está seleccionado
        if self.impuestos_seleccionados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False):
            tasa_impuesto = self.obtener_tasa_impuesto()
            # Descomponer el precio total en precio sin impuesto y impuesto
            precio_sin_impuesto_dolar = precio_total_dolar / (1 + tasa_impuesto)
        else:
            precio_sin_impuesto_dolar = precio_total_dolar

        # Verificar que el costo actual referencial no sea cero antes de calcular la utilidad
        if costo_actual_referencial == 0:
            # Manejar el caso de división por cero
            self.utilidad_dolar_edit_3.setText("0%")  # O cualquier otro manejo que desees
            return
        
        # Calcular la utilidad en base al costo actual referencial
        moneda_referencial = float(self.moneda_referencial_edit.text() or "0")
        precio_bs_sin_impuesto = float(self.precio_sin_impuesto_bs_edit.text() or "0")
        utilidad_dolar = round(
            (precio_sin_impuesto_dolar - costo_actual_referencial) / costo_actual_referencial,
            6  # Redondear a 4 decimales
        )
        precio_bs_sin_impuesto = precio_sin_impuesto_dolar * moneda_referencial
        utilidad_bs_monto = (precio_sin_impuesto_dolar - costo_actual_referencial) * moneda_referencial
        
        if self.impuestos_seleccionados.get("IMPUESTO AL VALOR AGREGADO (IVA 16%)", False):
            tasa_impuesto = self.obtener_tasa_impuesto()
            # Descomponer el precio total en precio sin impuesto y impuesto
            impuesto_bs = precio_bs_sin_impuesto * tasa_impuesto
        else:
            impuesto_bs = 0.00

        precio_total_bs = precio_bs_sin_impuesto + impuesto_bs

        # Actualizar los campos correspondientes
        self.precio_dolar_sin_impuesto_edit_3.setText(str(round(precio_sin_impuesto_dolar, 4)))
        self.utilidad_dolar_edit_3.setText(str(round(utilidad_dolar * 100, 4)) + "%")
        self.utilidad_bs_edit_3.setText(str(round(utilidad_dolar * 100, 4)) + "%")
        self.lineEdit_19.setText(str(round(utilidad_bs_monto, 4)))
        self.precio_sin_impuesto_bs_edit_3.setText(str(round((precio_bs_sin_impuesto), 2)))
        self.impuesto_total_bs_edit_3.setText(str(round((impuesto_bs), 2)))
        self.precio_total_bs_edit_3.setText(str(round((precio_total_bs), 2)))

    def restablecer_valor_predeterminado(self):
        if self.costo_actual_referencial_edit.text() == "":
            self.costo_actual_referencial_edit.setText("0.00")

    def obtener_tasa_impuesto(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT porcentaje FROM impuestos WHERE id = 1")  # Ajusta la consulta según tu esquema
        resultado = cursor.fetchone()
        
        conn.close()
        
        if resultado:
            return float(resultado[0])  # Devuelve la tasa de impuesto como un número flotante

    def calcular_costo(self, campo):
        input_str = campo.text()
        aeval = asteval.Interpreter()
        try:
            resultado = aeval(input_str)
            # Redondear el resultado a 4 decimales
            resultado_redondeado = round(resultado, 4)
            campo.setText(str(resultado_redondeado))
        except Exception as e:
            campo.setText("Error: " + str(e))

    def set_moneda_placeholder(self, line_edit, moneda):
        line_edit.setPlaceholderText(f'{moneda} ')

    def actualizar_costo_actual(self):
        if self.costo_actual_calculado:
            # Si el costo ya ha sido calculado, no hacemos nada
            return
        
        try:
            # Obtener el valor ingresado en costo_actual_referencial_edit
            costo_referencial = float(self.costo_actual_referencial_edit.text() or 0)

            # Obtener la tasa de conversión en moneda_referencial_edit
            tasa_conversion = float(self.moneda_referencial_edit.text() or 0)

            # Calcular el costo actual como el producto de costo_referencial y tasa_conversion
            costo_actual = costo_referencial * tasa_conversion

            # Actualizar el campo costo_actual_edit con el resultado
            self.costo_actual_edit.setText(str(round(costo_actual, 3)))

            # Marcar que el costo actual ha sido calculado
            self.costo_actual_calculado = True

        except ValueError:
            # Manejo de error si la conversión falla
            self.costo_actual_edit.setText("Entrada inválida")

    def cargar_moneda_referencial(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Obtener el factor de inventario de la moneda dólares
        cursor.execute("SELECT factor_inventario FROM monedas WHERE nombre = 'Dolares'")
        factor_inventario_dolares = cursor.fetchone()[0]

        # Asignar el valor a la variable moneda_referencial_edit
        self.moneda_referencial_edit.setText(str(factor_inventario_dolares))

        conn.close()

        self.recalcular_precios_bs_por_tasa(factor_inventario_dolares)

    def cambiar_estado_activo(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        query = """UPDATE productos_inventario SET activo = ? WHERE id = ?"""
        item = self.table_productos.item(self.table_productos.currentRow(), 0)
        if item is not None:
            cursor.execute(query, (self.activo_checkBox.isChecked(), item.text()))
        conn.commit()
        conn.close()

    def mostrar_mensaje_estado(self, Line_edit, mensaje):
        self.statusbar.showMessage(mensaje, 3000)  # Mostrar el mensaje durante 3 segundos

    def obtener_cantidad_productos(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        query = """SELECT COUNT(*) FROM productos_inventario"""
        cursor.execute(query)
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado[0] is not None else 0
        
    def actualizar_barra_estado(self):
        self.statusbar.showMessage(f"Productos creados: {self.obtener_cantidad_productos()}")

    def abrir_ventana_linea(self, texto):
        if texto == "Crear nueva linea":
            # Abre la ventana de marcas
            self.ventana_linea = ConfiguracionLinea()  
            self.ventana_linea.finished.connect(self.cargar_linea)  # Conecta la señal finished a la función cargar_linea
            self.ventana_linea.setWindowModality(QtCore.Qt.ApplicationModal)
            self.ventana_linea.show()

    def cargar_deposito(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Prepara la consulta SQL para seleccionar todos los códigos de depósitos
        query = """SELECT codigo FROM depositos"""

        # Ejecuta la consulta
        cursor.execute(query)

        # Limpia el combobox antes de agregar nuevas opciones
        self.deposito_comboBox.clear()

        # Obtiene todos los resultados de la consulta
        resultados = cursor.fetchall()

        # Agrega cada depósito al combobox
        for fila in resultados:
            self.deposito_comboBox.addItem(fila[0])  # fila[0] contiene el código del depósito

        # Cierra la conexión a la base de datos
        conn.close()

    def cargar_linea(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Prepara la consulta SQL para seleccionar todas las marcas
        query = """SELECT nombre FROM linea_inventario ORDER BY nombre"""

        # Ejecuta la consulta
        cursor.execute(query)

        # Limpia el combobox antes de agregar nuevas opciones
        self.linea_comboBox.clear()

        # Agrega las lineas al combobox
        row = cursor.fetchone()
        while row is not None:
            linea = row[0]
            self.linea_comboBox.addItem(linea)
            row = cursor.fetchone()

        # Agrega la opción "Crear linea"
        self.linea_comboBox.addItem("Crear nueva linea")

        # Cierra la conexión a la base de datos
        conn.close()

    def actualizar_linea(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Prepara la consulta SQL para actualizar la tabla productos_inventario con la nueva linea
        query = """UPDATE productos_inventario SET linea = (SELECT nombre FROM linea_inventario WHERE id = (SELECT MAX(id) FROM marcas)) WHERE marca IS NULL"""

        # Ejecuta la consulta
        cursor.execute(query)

        # Cierra la conexión a la base de datos
        conn.commit()
        conn.close()

    def abrir_ventana_marcas(self, texto):
        if texto == "Crear marca":
            # Abre la ventana de marcas
            self.ventana_marcas = ConfiguracionMarcas()  
            self.ventana_marcas.finished.connect(self.cargar_marcas)  # Conecta la señal finished a la función cargar_marcas
            self.ventana_marcas.setWindowModality(QtCore.Qt.ApplicationModal)
            self.ventana_marcas.show()

    def actualizar_marcas(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Prepara la consulta SQL para actualizar la tabla productos_inventario con la nueva marca
        query = """UPDATE productos_inventario SET marca = (SELECT nombre FROM marcas WHERE id = (SELECT MAX(id) FROM marcas)) WHERE marca IS NULL"""

        # Ejecuta la consulta
        cursor.execute(query)

        # Cierra la conexión a la base de datos
        conn.commit()
        conn.close()

    def cargar_marcas(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Prepara la consulta SQL para seleccionar todas las marcas
        query = """SELECT nombre FROM marcas ORDER BY nombre"""

        # Ejecuta la consulta
        cursor.execute(query)

        # Limpia el combobox antes de agregar nuevas opciones
        self.marca_comboBox.clear()

        # Agrega las marcas al combobox
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            marca = row[0]
            self.marca_comboBox.addItem(marca)

        # Agrega la opción "Crear marca"
        self.marca_comboBox.addItem("Crear marca")

        # Llamar al método cargar_moneda_referencial
        self.cargar_moneda_referencial()

        # Cierra la conexión a la base de datos
        conn.close()

    def habilitar_campos(self):
        self.descripcion_edit.clear()
        self.unidad_edit.setText("1")
        self.paquete_edit.clear()
        self.activo_checkBox.setChecked(True)
        self.costo_anterior_edit.clear()
        self.costo_actual_edit.clear()
        self.costo_promedio_edit.clear()
        self.costo_reposicion_edit.clear()
        self.moneda_referencial_edit.setDisabled(True)
        self.costo_actual_referencial_edit.clear()

        self.utilidad_bs_edit.setText("0%")
        self.utilidad_bs_edit_2.setText("0%")
        self.utilidad_bs_edit_3.setText("0%")
        self.precio_sin_impuesto_bs_edit.setText("0.00")
        self.precio_sin_impuesto_bs_edit_2.setText("0.00")
        self.precio_sin_impuesto_bs_edit_3.setText("0.00")
        self.impuesto_total_bs_edit.setText("0.00")
        self.impuesto_total_bs_edit_2.setText("0.00")
        self.impuesto_total_bs_edit_3.setText("0.00")
        self.precio_total_bs_edit.setText("0.00")
        self.precio_total_bs_edit_2.setText("0.00")
        self.precio_total_bs_edit_3.setText("0.00")
        self.lineEdit_17.setText("0.00")
        self.lineEdit_18.setText("0.00")
        self.lineEdit_19.setText("0.00")
        self.utilidad_dolar_edit.setText("0%")
        self.utilidad_dolar_edit_2.setText("0%")
        self.utilidad_dolar_edit_3.setText("0%")
        self.precio_dolar_sin_impuesto_edit.setText("0.00")
        self.precio_dolar_sin_impuesto_edit_2.setText("0.00")
        self.precio_dolar_sin_impuesto_edit_3.setText("0.00")
        self.precio_total_dolar_edit.setText("0.00")
        self.precio_total_dolar_edit_2.setText("0.00")
        self.precio_total_dolar_edit_3.setText("0.00")

        self.peso_litro_edit.clear()
        self.existencia_maxima_edit.clear()
        self.existencia_minima_edit.setText("1")
        self.codigo_barra_edit.clear()

        # Habilita los campos de entrada
        self.codigo_edit.setDisabled(False)
        self.descripcion_edit.setDisabled(False)
        self.unidad_edit.setDisabled(False)
        self.unidad_edit.setText("1")
        self.paquete_edit.setDisabled(False)
        self.activo_checkBox.setChecked(True)
        self.costo_anterior_edit.setDisabled(False)
        self.costo_actual_edit.setDisabled(False)
        self.costo_promedio_edit.setDisabled(False)
        self.costo_reposicion_edit.setDisabled(False)
        self.moneda_referencial_edit.setDisabled(True)
        self.costo_actual_referencial_edit.setDisabled(False)
        self.utilidad_bs_edit.setDisabled(False)
        self.precio_sin_impuesto_bs_edit.setDisabled(False)
        self.impuesto_total_bs_edit.setDisabled(False)
        self.precio_total_bs_edit.setDisabled(False)
        self.lineEdit_17.setDisabled(False)
        self.utilidad_dolar_edit.setDisabled(False)
        self.precio_dolar_sin_impuesto_edit.setDisabled(False)
        self.precio_total_dolar_edit.setDisabled(False)
        self.utilidad_bs_edit_2.setDisabled(False)
        self.precio_sin_impuesto_bs_edit_2.setDisabled(False)
        self.impuesto_total_bs_edit_2.setDisabled(False)
        self.precio_total_bs_edit_2.setDisabled(False)
        self.lineEdit_18.setDisabled(False)
        self.utilidad_dolar_edit_2.setDisabled(False)
        self.precio_dolar_sin_impuesto_edit_2.setDisabled(False)
        self.precio_total_dolar_edit_2.setDisabled(False)
        self.utilidad_bs_edit_3.setDisabled(False)
        self.precio_sin_impuesto_bs_edit_3.setDisabled(False)
        self.impuesto_total_bs_edit_3.setDisabled(False)
        self.precio_total_bs_edit_3.setDisabled(False)
        self.lineEdit_19.setDisabled(False)
        self.utilidad_dolar_edit_3.setDisabled(False)
        self.precio_dolar_sin_impuesto_edit_3.setDisabled(False)
        self.precio_total_dolar_edit_3.setDisabled(False)
        self.peso_litro_edit.setDisabled(False)
        self.existencia_maxima_edit.setDisabled(False)
        self.existencia_minima_edit.setDisabled(False)
        self.existencia_minima_edit.setText("1")
        self.codigo_barra_edit.setDisabled(False)
        self.moneda_listView.setDisabled(True)
        self.moneda_ref_listView.setDisabled(True)

        # Habilita los QComboBox
        self.marca_comboBox.setDisabled(False)
        self.linea_comboBox.setDisabled(False)
        self.deposito_comboBox.setDisabled(False)

        # Habilita los checkbox
        self.activo_checkBox.setDisabled(False)

        # Limpia la imagen del QGraphicsView
        self.imagen_scene.clear()
        self.imagen_producto_graphicsView.setScene(self.imagen_scene)

        # Habilita los botones "Añadir" y "Borrar"
        self.button_anadir.setDisabled(False)
        self.button_borrar.setDisabled(False)
        self.button_cancelar.setDisabled(False)
        self.button_impuestos.setDisabled(False)
        # Cambia el texto del botón "Crear" a "Guardar Producto"
        self.button_crear.setText("Guardar")
        self.button_crear.clicked.disconnect()
        self.button_crear.clicked.connect(self.guardar_nuevo_producto)

    def guardar_nuevo_producto(self):
        # Conecta a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        codigo = self.codigo_edit.text()

        # Check if required fields are filled in
        for campo in self.campos_obligatorios():
            if isinstance(campo, QtWidgets.QLineEdit):
                if campo.text() == "":
                    QMessageBox.critical(None, "Error", "Los campos obligatorios no pueden estar vacíos.")
                    return
            elif isinstance(campo, QtWidgets.QComboBox):
                if campo.currentText() == "":
                    QMessageBox.critical(None, "Error", "Los campos obligatorios no pueden estar vacíos.")
                    return

        # Verifica si el producto ya existe en la base de datos
        query = "SELECT * FROM productos_inventario WHERE codigo = ?"
        cursor.execute(query, (self.codigo_edit.text(),))
        resultado = cursor.fetchone()

        if resultado is None:
            # Obtener los valores seleccionados en los combobox de marca y línea
            marca = self.marca_comboBox.currentText()
            linea = self.linea_comboBox.currentText()
            deposito = self.deposito_comboBox.currentText()

            # Inserta el producto en la base de datos
            query = """INSERT INTO productos_inventario (
                codigo,
                descripcion,
                unidad,
                paquete,
                costo_anterior,
                costo_actual,
                costo_promedio,
                costo_reposicion,
                moneda_referencial,
                costo_actual_referencial,
                utilidad_bs,
                utilidad_bs_2,
                utilidad_bs_3,
                monto_utilidad_bs,
                monto_utilidad_bs_2,
                monto_utilidad_bs_3,
                precio_sin_impuesto_bs,
                precio_sin_impuesto_bs_2,
                precio_sin_impuesto_bs_3,
                impuesto_total_bs,
                impuesto_total_bs_2,
                impuesto_total_bs_3,
                precio_total_bs,
                precio_total_bs_2,
                precio_total_bs_3,
                utilidad_dolar,
                utilidad_dolar_2,
                utilidad_dolar_3,
                precio_sin_impuesto_dolar,
                precio_sin_impuesto_dolar_2,
                precio_sin_impuesto_dolar_3,
                precio_total_dolar,
                precio_total_dolar_2,
                precio_total_dolar_3,
                peso_litro,
                existencia_maxima,
                existencia_minima,
                codigo_barra,
                marca,
                linea,
                deposito,
                activo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            fields = [
                ("codigo", self.codigo_edit),
                ("descripcion", self.descripcion_edit),
                ("unidad", self.unidad_edit),
                ("paquete", self.paquete_edit),
                ("costo_anterior", self.costo_anterior_edit),
                ("costo_actual", self.costo_actual_edit),
                ("costo_promedio", self.costo_promedio_edit),
                ("costo_reposicion", self.costo_reposicion_edit),
                ("moneda_referencial", self.moneda_referencial_edit),
                ("costo_actual_referencial", self.costo_actual_referencial_edit),
                ("utilidad_bs", self.utilidad_bs_edit),
                ("utilidad_bs_2", self.utilidad_bs_edit_2),
                ("utilidad_bs_3", self.utilidad_bs_edit_3),
                ("monto_utilidad_bs", self.lineEdit_17),
                ("monto_utilidad_bs_2", self.lineEdit_18),
                ("monto_utilidad_bs_3", self.lineEdit_19),
                ("precio_sin_impuesto_bs", self.precio_sin_impuesto_bs_edit),
                ("precio_sin_impuesto_bs_2", self.precio_sin_impuesto_bs_edit_2),
                ("precio_sin_impuesto_bs_3", self.precio_sin_impuesto_bs_edit_3),
                ("impuesto_total_bs", self.impuesto_total_bs_edit),
                ("impuesto_total_bs_2", self.impuesto_total_bs_edit_2),
                ("impuesto_total_bs_3", self.impuesto_total_bs_edit_3),
                ("precio_total_bs", self.precio_total_bs_edit),
                ("precio_total_bs_2", self.precio_total_bs_edit_2),
                ("precio_total_bs_3", self.precio_total_bs_edit_3),
                ("utilidad_dolar", self.utilidad_dolar_edit),
                ("utilidad_dolar_2", self.utilidad_dolar_edit_2),
                ("utilidad_dolar_3", self.utilidad_dolar_edit_3),
                ("precio_sin_impuesto_dolar", self.precio_dolar_sin_impuesto_edit),
                ("precio_sin_impuesto_dolar_2", self.precio_dolar_sin_impuesto_edit_2),
                ("precio_sin_impuesto_dolar_3", self.precio_dolar_sin_impuesto_edit_3),
                ("precio_total_dolar", self.precio_total_dolar_edit),
                ("precio_total_dolar_2", self.precio_total_dolar_edit_2),
                ("precio_total_dolar_3", self.precio_total_dolar_edit_3),
                ("peso_litro", self.peso_litro_edit),
                ("existencia_maxima", self.existencia_maxima_edit),
                ("existencia_minima", self.existencia_minima_edit),
                ("codigo_barra", self.codigo_barra_edit),
                ("marca", self.marca_comboBox),
                ("linea", self.linea_comboBox),
                ("deposito", self.deposito_comboBox),
                ("activo", self.activo_checkBox.isChecked())
            ]
            valores = []
            for field, edit in fields:
                if hasattr(edit, 'text'):
                    valores.append(edit.text())
                elif hasattr(edit, 'currentText'):
                    valores.append(edit.currentText())
                elif isinstance(edit, bool):
                    valores.append(str(edit))
                else:
                    valores.append('')
            cursor.execute(query, valores)

        self.table_productos.setDisabled(False)

        # Obtén el último ID insertado
        last_id = cursor.lastrowid

        # Selecciona el producto recién insertado en la tabla
        if self.imagen_scene.items():
            # Obtiene el pixmap del primer item
            pixmap = self.imagen_scene.items()[0].pixmap()
            
            # Verifica si el pixmap no está vacío
            if not pixmap.isNull():
                imagen_nombre = f"producto_{codigo}.png"
                imagen_ruta_guardar = os.path.join(os.getcwd(), "imagen_productos", imagen_nombre)
                
                # Intenta guardar la imagen y maneja posibles errores
                try:
                    pixmap.save(imagen_ruta_guardar, "png")
                    print(f"Imagen guardada en: {imagen_ruta_guardar}")  # Mensaje de éxito
                except Exception as e:
                    print(f"Error al guardar la imagen: {e}")  # Mensaje de error
            else:
                print("El pixmap está vacío. No se puede guardar la imagen.")  # Mensaje de advertencia
        else:
            print("No hay imagen seleccionada para guardar.")  # Mensaje si no hay imagen

        self.guardar_impuestos(codigo)

        # Cierra la conexión a la base de datos
        conn.commit()
        conn.close()

        # Limpia la escena de la imagen
        self.imagen_scene.clear()  
        self.imagen_producto_graphicsView.setScene(self.imagen_scene)  # Asegúrate de actualizar el QGraphicsView

        # Limpia los campos de entrada, combobox y la imagen
        self.codigo_edit.clear()
        self.limpiar_campos()
        self.cargar_productos_en_tabla()

        #Deshabilita los botones "Añadir" y "Borrar"
        self.button_anadir.setDisabled(True)
        self.button_borrar.setDisabled(True)

        self.button_crear.setText("Crear")
        self.button_crear.clicked.disconnect()
        self.button_crear.clicked.connect(self.habilitar_codigo)

        # Deshabilita los campos y combobox
        self.codigo_edit.setDisabled(True)
        self.descripcion_edit.setDisabled(True)
        self.unidad_edit.setDisabled(True)
        self.paquete_edit.setDisabled(True)
        self.activo_checkBox.setDisabled(True)
        self.costo_anterior_edit.setDisabled(True)
        self.costo_actual_edit.setDisabled(True)
        self.costo_promedio_edit.setDisabled(True)
        self.costo_reposicion_edit.setDisabled(True)
        self.moneda_referencial_edit.setDisabled(True)
        self.costo_actual_referencial_edit.setDisabled(True)
        self.utilidad_bs_edit.setDisabled(True)
        self.precio_sin_impuesto_bs_edit.setDisabled(True)
        self.impuesto_total_bs_edit.setDisabled(True)
        self.precio_total_bs_edit.setDisabled(True)
        self.lineEdit_17.setDisabled(True)
        self.utilidad_dolar_edit.setDisabled(True)
        self.precio_dolar_sin_impuesto_edit.setDisabled(True)
        self.precio_total_dolar_edit.setDisabled(True)
        self.utilidad_bs_edit_2.setDisabled(True)
        self.precio_sin_impuesto_bs_edit_2.setDisabled(True)
        self.impuesto_total_bs_edit_2.setDisabled(True)
        self.precio_total_bs_edit_2.setDisabled(True)
        self.lineEdit_18.setDisabled(True)
        self.utilidad_dolar_edit_2.setDisabled(True)
        self.precio_dolar_sin_impuesto_edit_2.setDisabled(True)
        self.precio_total_dolar_edit_2.setDisabled(True)
        self.utilidad_bs_edit_3.setDisabled(True)
        self.precio_sin_impuesto_bs_edit_3.setDisabled(True)
        self.impuesto_total_bs_edit_3.setDisabled(True)
        self.precio_total_bs_edit_3.setDisabled(True)
        self.lineEdit_19.setDisabled(True)
        self.utilidad_dolar_edit_3.setDisabled(True)
        self.precio_dolar_sin_impuesto_edit_3.setDisabled(True)
        self.precio_total_dolar_edit_3.setDisabled(True)
        self.peso_litro_edit.setDisabled(True)
        self.existencia_maxima_edit.setDisabled(True)
        self.existencia_minima_edit.setDisabled(True)
        self.codigo_barra_edit.setDisabled(True)
        self.marca_comboBox.setDisabled(True)
        self.linea_comboBox.setDisabled(True)
        self.deposito_comboBox.setDisabled(True)
        self.button_impuestos.setDisabled(True)

    def guardar_impuestos(self, codigo_producto):
        # Agregar o actualizar los impuestos del producto en el diccionario
        self.productos_impuestos[codigo_producto] = self.impuestos_seleccionados

        # Guardar el diccionario en un archivo JSON
        with open('productos_impuestos.json', 'w') as f:
            json.dump(self.productos_impuestos, f)

    def cargar_impuestos(self):
        # Cargar impuestos desde el archivo JSON
        if os.path.exists('productos_impuestos.json'):
            with open('productos_impuestos.json', 'r') as f:
                self.productos_impuestos = json.load(f)
        else:
            self.productos_impuestos = {}  # Si el archivo no existe, inicializa como vacío

    def guardar_producto_modificado(self):
        # Obtener el código del producto modificado
        codigo = self.codigo_edit.text()

        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Actualizar el producto en la base de datos
        query = """UPDATE productos_inventario SET
                    descripcion = ?,
                    unidad = ?,
                    paquete = ?,
                    costo_anterior = ?,
                    costo_actual = ?,
                    costo_promedio = ?,
                    costo_reposicion = ?,
                    costo_actual_referencial = ?,
                    utilidad_bs = ?,
                    utilidad_bs_2 = ?,
                    utilidad_bs_3 = ?,
                    monto_utilidad_bs = ?,
                    monto_utilidad_bs_2 = ?,
                    monto_utilidad_bs_3 = ?,
                    precio_sin_impuesto_bs = ?,
                    precio_sin_impuesto_bs_2 = ?,
                    precio_sin_impuesto_bs_3 = ?,
                    impuesto_total_bs = ?,
                    impuesto_total_bs_2 = ?,
                    impuesto_total_bs_3 = ?,
                    precio_total_bs = ?,
                    precio_total_bs_2 = ?,
                    precio_total_bs_3 = ?,
                    utilidad_dolar = ?,
                    utilidad_dolar_2 = ?,
                    utilidad_dolar_3 = ?,
                    precio_sin_impuesto_dolar = ?,
                    precio_sin_impuesto_dolar_2 = ?,
                    precio_sin_impuesto_dolar_3 = ?,
                    precio_total_dolar = ?,
                    precio_total_dolar_2 = ?,
                    precio_total_dolar_3 = ?,
                    peso_litro = ?,
                    existencia_maxima = ?,
                    existencia_minima = ?,
                    codigo_barra = ?,
                    marca = ?,
                    linea = ?,
                    deposito = ?,
                    activo = ?
                    WHERE codigo = ?"""
        # Asegúrate de que el valor sea convertible a float
        try:
            valor_lineEdit_19 = self.lineEdit_19.text()
            if valor_lineEdit_19 and valor_lineEdit_19 != 'None':
                valor_lineEdit_19 = float(valor_lineEdit_19)
            else:
                valor_lineEdit_19 = 0.0  # O el valor que desees asignar en caso de que el campo esté vacío o sea 'None'
        except ValueError:
            print("Error al convertir el valor de lineEdit_19 a float.")
            valor_lineEdit_19 = 0.0  # O maneja el error como prefieras

        valores = [
            self.descripcion_edit.text(),
            self.unidad_edit.text(),
            self.paquete_edit.text(),
            str(self.costo_anterior_edit.text()),
            str(self.costo_actual_edit.text()),
            str(self.costo_promedio_edit.text()),
            str(self.costo_reposicion_edit.text()),
            float(self.costo_actual_referencial_edit.text()),
            str(self.utilidad_bs_edit.text()),
            str(self.utilidad_bs_edit_2.text()),
            str(self.utilidad_bs_edit_3.text()),
            str(self.lineEdit_17.text()),
            str(self.lineEdit_18.text()),
            valor_lineEdit_19,  # Aquí se usa el valor ya procesado
            float(self.precio_sin_impuesto_bs_edit.text()),
            float(self.precio_sin_impuesto_bs_edit_2.text()),
            float(self.precio_sin_impuesto_bs_edit_3.text()),
            float(self.impuesto_total_bs_edit.text()),
            float(self.impuesto_total_bs_edit_2.text()),
            float(self.impuesto_total_bs_edit_3.text()),
            float(self.precio_total_bs_edit.text()),
            float(self.precio_total_bs_edit_2.text()),
            float(self.precio_total_bs_edit_3.text()),
            str(self.utilidad_dolar_edit.text()),
            str(self.utilidad_dolar_edit_2.text()),
            str(self.utilidad_dolar_edit_3.text()),
            float(self.precio_dolar_sin_impuesto_edit.text()),
            float(self.precio_dolar_sin_impuesto_edit_2.text()),
            float(self.precio_dolar_sin_impuesto_edit_3.text()),
            float(self.precio_total_dolar_edit.text()),
            float(self.precio_total_dolar_edit_2.text()),
            float(self.precio_total_dolar_edit_3.text()),
            str(self.peso_litro_edit.text()),
            str(self.existencia_maxima_edit.text()),
            str(self.existencia_minima_edit.text()),
            self.codigo_barra_edit.text(),
            self.marca_comboBox.currentText(),
            self.linea_comboBox.currentText(),
            self.deposito_comboBox.currentText(),
            self.activo_checkBox.isChecked(),
            codigo
        ]
        self.guardar_impuestos(codigo)

        # Selecciona el producto recién insertado en la tabla
        if self.imagen_scene.items():
            # Obtiene el pixmap del primer item
            pixmap = self.imagen_scene.items()[0].pixmap()
            
            # Verifica si el pixmap no está vacío
            if not pixmap.isNull():
                imagen_nombre = f"producto_{codigo}.png"
                imagen_ruta_guardar = os.path.join(os.getcwd(), "imagen_productos", imagen_nombre)
                
                # Intenta guardar la imagen y maneja posibles errores
                try:
                    pixmap.save(imagen_ruta_guardar, "png")
                    print(f"Imagen guardada en: {imagen_ruta_guardar}")  # Mensaje de éxito
                except Exception as e:
                    print(f"Error al guardar la imagen: {e}")  # Mensaje de error
            else:
                print("El pixmap está vacío. No se puede guardar la imagen.")  # Mensaje de advertencia
        else:
            print("No hay imagen seleccionada para guardar.")  # Mensaje si no hay imagen

        try:
            cursor.execute(query, valores) 
            conn.commit()  # Asegúrate de confirmar los cambios
            print("Producto modificado exitosamente")  # Mensaje de éxito
        except Exception as e:
            print("Error al modificar el producto:", e)  # Captura y muestra el error
        finally:
            conn.close()  # Cierra la conexión a la base de datos

        # Habilitar la tabla
        self.table_productos.setEnabled(True)

        # Deshabilitar los campos de entrada, combobox y vista de la foto
        self.codigo_edit.setEnabled(False) 
        self.descripcion_edit.setEnabled(False) 
        self.unidad_edit.setEnabled(False) 
        self.paquete_edit.setEnabled(False) 
        self.costo_anterior_edit.setEnabled(False) 
        self.costo_actual_edit.setEnabled(False) 
        self.costo_promedio_edit.setEnabled(False) 
        self.costo_reposicion_edit.setEnabled(False) 
        self.costo_actual_referencial_edit.setEnabled(False) 
        self.utilidad_bs_edit.setEnabled(False) 
        self.utilidad_bs_edit_2.setEnabled(False) 
        self.utilidad_bs_edit_3.setEnabled(False) 
        self.lineEdit_17.setEnabled(False) 
        self.lineEdit_18.setEnabled(False) 
        self.lineEdit_19.setEnabled(False) 
        self.precio_sin_impuesto_bs_edit.setEnabled(False) 
        self.precio_sin_impuesto_bs_edit_2.setEnabled(False) 
        self.precio_sin_impuesto_bs_edit_3.setEnabled(False) 
        self.impuesto_total_bs_edit.setEnabled(False) 
        self.impuesto_total_bs_edit_2.setEnabled(False) 
        self.impuesto_total_bs_edit_3.setEnabled(False) 
        self.precio_total_bs_edit.setEnabled(False) 
        self.precio_total_bs_edit_2.setEnabled(False) 
        self.precio_total_bs_edit_3.setEnabled(False) 
        self.utilidad_dolar_edit.setEnabled(False) 
        self.utilidad_dolar_edit_2.setEnabled(False) 
        self.utilidad_dolar_edit_3.setEnabled(False) 
        self.precio_dolar_sin_impuesto_edit.setEnabled(False) 
        self.precio_dolar_sin_impuesto_edit_2.setEnabled(False) 
        self.precio_dolar_sin_impuesto_edit_3.setEnabled(False) 
        self.precio_total_dolar_edit.setEnabled(False) 
        self.precio_total_dolar_edit_2.setEnabled(False) 
        self.precio_total_dolar_edit_3.setEnabled(False) 
        self.peso_litro_edit.setEnabled(False)
        self.existencia_maxima_edit.setEnabled(False) 
        self.existencia_minima_edit.setEnabled(False) 
        self.codigo_barra_edit.setEnabled(False) 
        self.marca_comboBox.setEnabled(False) 
        self.linea_comboBox.setEnabled(False) 
        self.deposito_comboBox.setDisabled(True)
        self.activo_checkBox.setEnabled(False)
        self.button_anadir.setDisabled(True)
        self.button_borrar.setDisabled(True)
        self.button_impuestos.setDisabled(True)

        # Limpiar los campos después de guardar
        self.limpiar_campos()
        self.codigo_edit.clear()

        # Restablecer el botón a su estado original
        self.button_modificar.setText("Modificar") 
        self.button_modificar.disconnect()  # Desconectar la señal actual
        self.button_modificar.clicked.connect(self.modificar_producto)  # Volver a conectar a la función de modificar

        # Actualizar la tabla de productos
        self.cargar_productos_en_tabla()

    def mostrar_mensaje(self, mensaje):
        QMessageBox.information(self, "Información", mensaje, QMessageBox.Ok)

    def modificar_producto(self):
        print("Entrando en la función modificar_producto")
        # Obtén el índice de la fila seleccionada
        indice = self.table_productos.selectionModel().currentIndex().row()
        print("Índice de la fila seleccionada:", indice)

        # Verifica si el índice es válido
        if indice != -1:
            print("Índice válido")
            # Limpia los campos de entrada, combobox y graphic view
            self.limpiar_campos()
            self.imagen_scene.clear()
            self.imagen_producto_graphicsView.setScene(self.imagen_scene)

            # Obtén el código del producto seleccionado
            item = self.table_productos.item(indice, 0)
            if item is not None:
                print("Código del producto seleccionado:", item.text())
                codigo = item.text()

                # Conecta a la base de datos
                conn = sqlite3.connect('Usuarios.db')
                cursor = conn.cursor()

                # Prepara la consulta SQL para seleccionar el producto
                query = """SELECT * FROM productos_inventario WHERE codigo = ?"""
                cursor.execute(query, (codigo,))
            
                # Iterar sobre los resultados y llenar los campos
                row = cursor.fetchone()
                if row is not None:
                    # Cargar los campos de entrada
                    self.codigo_edit.setText(row[1])
                    self.descripcion_edit.setText(row[2])
                    self.unidad_edit.setText(row[5])
                    self.paquete_edit.setText(row[6])
                    self.costo_anterior_edit.setText(str(row[7]))
                    self.costo_actual_edit.setText(str(row[8]))
                    self.costo_promedio_edit.setText(str(row[9]))
                    self.costo_reposicion_edit.setText(str(row[10]))
                    self.costo_actual_referencial_edit.setText(str(row[12]))
                    self.utilidad_bs_edit.setText(str(row[13]))
                    self.utilidad_bs_edit_2.setText(str(row[20]))
                    self.utilidad_bs_edit_3.setText(str(row[27]))
                    self.lineEdit_17.setText(str(row[40]))
                    self.lineEdit_18.setText(str(row[41]))
                    self.lineEdit_19.setText(str(row[42]))
                    self.precio_sin_impuesto_bs_edit.setText(str(row[14]))
                    self.precio_sin_impuesto_bs_edit_2.setText(str(row[21]))
                    self.precio_sin_impuesto_bs_edit_3.setText(str(row[28]))
                    self.impuesto_total_bs_edit.setText(str(row[15]))
                    self.impuesto_total_bs_edit_2.setText(str(row[22]))
                    self.impuesto_total_bs_edit_3.setText(str(row[29]))
                    self.precio_total_bs_edit.setText(str(row[16]))
                    self.precio_total_bs_edit_2.setText(str(row[23]))
                    self.precio_total_bs_edit_3.setText(str(row[30]))
                    self.utilidad_dolar_edit.setText(str(row[17]))
                    self.utilidad_dolar_edit_2.setText(str(row[24]))
                    self.utilidad_dolar_edit_3.setText(str(row[37]))
                    self.precio_dolar_sin_impuesto_edit.setText(str(row[18]))
                    self.precio_dolar_sin_impuesto_edit_2.setText(str(row[25]))
                    self.precio_dolar_sin_impuesto_edit_3.setText(str(row[38]))
                    self.precio_total_dolar_edit.setText(str(row[19]))
                    self.precio_total_dolar_edit_2.setText(str(row[26]))
                    self.precio_total_dolar_edit_3.setText(str(row[39]))
                    self.peso_litro_edit.setText(str(row[31]))
                    self.existencia_maxima_edit.setText(str(row[33]))
                    self.existencia_minima_edit.setText(str(row[34]))
                    self.codigo_barra_edit.setText(str(row[35]))

                    # Cargar los combobox
                    self.marca_comboBox.setCurrentText(row[3])
                    self.linea_comboBox.setCurrentText(row[4])
                    self.deposito_comboBox.setCurrentText(row[43])

                    self.activo_checkBox.setChecked(bool(row[36]))

                    # Cargar la imagen
                    imagen_ruta = f"imagen_productos/producto_{codigo}.png"
                    pixmap = QPixmap(imagen_ruta)
                    item = QGraphicsPixmapItem(pixmap)
                    self.imagen_scene.addItem(item)
                    self.imagen_producto_graphicsView.setScene(self.imagen_scene)
                else: 
                    print("No se encontró el producto en la base de datos.") 
            else: 
                print("No se pudo obtener el código del producto seleccionado.") 
        else: 
            print("Índice no válido, no se puede modificar el producto.") 
            
        # Cierra la conexión a la base de datos
        conn.close()
        # Deshabilitar la tabla
        self.table_productos.setDisabled(True)

        # Habilitar campos, combobox, graphic view y checkbox
        self.codigo_edit.setDisabled(False)
        self.descripcion_edit.setDisabled(False)
        self.unidad_edit.setDisabled(False)
        self.paquete_edit.setDisabled(False)
        self.existencia_maxima_edit.setDisabled(False)
        self.peso_litro_edit.setDisabled(False)
        self.codigo_barra_edit.setDisabled(False)
        self.activo_checkBox.setDisabled(False)
        self.costo_anterior_edit.setDisabled(False)
        self.costo_actual_edit.setDisabled(False)
        self.costo_promedio_edit.setDisabled(False)
        self.costo_reposicion_edit.setDisabled(False)
        self.costo_actual_referencial_edit.setDisabled(False)
        self.utilidad_bs_edit.setDisabled(False)
        self.utilidad_bs_edit_2.setDisabled(False)
        self.utilidad_bs_edit_3.setDisabled(False)
        self.precio_sin_impuesto_bs_edit.setDisabled(False)
        self.precio_sin_impuesto_bs_edit_2.setDisabled(False)
        self.precio_sin_impuesto_bs_edit_3.setDisabled(False)
        self.impuesto_total_bs_edit.setDisabled(False)
        self.impuesto_total_bs_edit_2.setDisabled(False)
        self.impuesto_total_bs_edit_3.setDisabled(False)
        self.precio_total_bs_edit.setDisabled(False)
        self.precio_total_bs_edit_2.setDisabled(False)
        self.precio_total_bs_edit_3.setDisabled(False)
        self.utilidad_dolar_edit.setDisabled(False)
        self.utilidad_dolar_edit_2.setDisabled(False)
        self.utilidad_dolar_edit_3.setDisabled(False)
        self.precio_dolar_sin_impuesto_edit.setDisabled(False)
        self.precio_dolar_sin_impuesto_edit_2.setDisabled(False)
        self.precio_dolar_sin_impuesto_edit_3.setDisabled(False)
        self.precio_total_dolar_edit.setDisabled(False)
        self.precio_total_dolar_edit_2.setDisabled(False)
        self.precio_total_dolar_edit_3.setDisabled(False)
        self.marca_comboBox.setDisabled(False)
        self.linea_comboBox.setDisabled(False)
        self.deposito_comboBox.setDisabled(False)
        self.imagen_producto_graphicsView.setDisabled(False)
        self.button_anadir.setDisabled(False)
        self.button_borrar.setDisabled(False)
        self.button_impuestos.setDisabled(False)

        self.costo_actual_calculado = True

        self.button_modificar.setText("Guardar")
        self.button_modificar.clicked.disconnect()
        self.button_modificar.clicked.connect(self.guardar_producto_modificado)
        self.button_delete.setDisabled(True)
        self.button_cancelar.setDisabled(False)
        self.codigo_edit.setDisabled(True)

    def campos_obligatorios(self):
        return [
            self.codigo_edit,
            self.descripcion_edit,
            self.unidad_edit,
            self.marca_comboBox,
            self.existencia_minima_edit,
            self.existencia_maxima_edit,
            self.costo_actual_referencial_edit,
            self.utilidad_dolar_edit,
            self.utilidad_dolar_edit_2,
            self.utilidad_dolar_edit_3
        ]

    def limpiar_campos(self):
        # Limpia los campos de entrada
        self.descripcion_edit.clear()
        self.unidad_edit.setText("1")
        self.paquete_edit.clear()
        self.activo_checkBox.setChecked(True)
        self.costo_anterior_edit.clear()
        self.costo_actual_edit.clear()
        self.costo_promedio_edit.clear()
        self.costo_reposicion_edit.clear()
        self.moneda_referencial_edit.setDisabled(True)
        self.costo_actual_referencial_edit.clear()
        self.utilidad_bs_edit.setText("0%")
        self.utilidad_bs_edit_2.setText("0%")
        self.utilidad_bs_edit_3.setText("0%")
        self.precio_sin_impuesto_bs_edit.setText("0.00")
        self.precio_sin_impuesto_bs_edit_2.setText("0.00")
        self.precio_sin_impuesto_bs_edit_3.setText("0.00")
        self.impuesto_total_bs_edit.setText("0.00")
        self.impuesto_total_bs_edit_2.setText("0.00")
        self.impuesto_total_bs_edit_3.setText("0.00")
        self.precio_total_bs_edit.setText("0.00")
        self.precio_total_bs_edit_2.setText("0.00")
        self.precio_total_bs_edit_3.setText("0.00")
        self.lineEdit_17.setText("0.00")
        self.lineEdit_18.setText("0.00")
        self.lineEdit_19.setText("0.00")
        self.utilidad_dolar_edit.setText("0%")
        self.utilidad_dolar_edit_2.setText("0%")
        self.utilidad_dolar_edit_3.setText("0%")
        self.precio_dolar_sin_impuesto_edit.setText("0.00")
        self.precio_dolar_sin_impuesto_edit_2.setText("0.00")
        self.precio_dolar_sin_impuesto_edit_3.setText("0.00")
        self.precio_total_dolar_edit.setText("0.00")
        self.precio_total_dolar_edit_2.setText("0.00")
        self.precio_total_dolar_edit_3.setText("0.00")
        self.peso_litro_edit.clear()
        self.existencia_maxima_edit.clear()
        self.existencia_minima_edit.setText("1")
        self.codigo_barra_edit.clear()
        
        # Limpia los combobox
        self.marca_comboBox.setCurrentIndex(0)
        self.linea_comboBox.setCurrentIndex(0)
        self.deposito_comboBox.setCurrentIndex(0)
        
        # Limpia la imagen
        self.imagen_scene.clear()
        self.imagen_producto_graphicsView.setScene(self.imagen_scene)
        self.imagen_ruta = ""

    def eliminar_producto(self):
        # Obtén el índice de la fila seleccionada
        row = self.table_productos.currentRow()
        
        # Si no se ha seleccionado ninguna fila, no hagas nada
        if row == -1:
            return
        
        # Pregúntale al usuario si desea eliminar el producto
        respuesta = QMessageBox.question(self, "Eliminar producto", "¿Seguro que deseas eliminar este producto?", QMessageBox.Yes | QMessageBox.No)

        # Si el usuario responde que sí, elimina el producto
        if respuesta == QMessageBox.Yes:
            # Obtén el código del producto seleccionado
            item = self.table_productos.item(row, 0)
            if item is not None:
                codigo = item.text()
        
                # Conecta a la base de datos
                conn = sqlite3.connect('Usuarios.db')
                cursor = conn.cursor()
                
                # Elimina el producto de la base de datos
                query = "DELETE FROM productos_inventario WHERE codigo = ?"
                cursor.execute(query, (codigo,))
                
                # Confirma los cambios
                conn.commit()
                
                # Cierra la conexión a la base de datos
                conn.close()

                # Eliminar la imagen del producto
                imagen_ruta = f"imagen_productos/producto_{codigo}.png"
                if os.path.exists(imagen_ruta):
                    os.remove(imagen_ruta)  # Elimina la imagen
                
                # Actualiza la tabla para reflejar los cambios
                self.cargar_productos_en_tabla()

    def cargar_productos_en_tabla(self):
        # Limpia la tabla
        self.table_productos.setRowCount(0)

        # Conecta a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Prepara la consulta SQL para seleccionar todos los productos
        query = """
        SELECT p.codigo, p.descripcion, p.marca, e.cantidad, p.precio_total_bs, p.precio_total_dolar 
        FROM productos_inventario p
        LEFT JOIN existencia_productos e ON p.codigo = e.codigo
        """

        # Ejecuta la consulta
        cursor.execute(query)

        # Función para formatear los montos
        def formato_monto(valor):
            try:
                # Convertir a float y formatear con 2 decimales y separadores de miles
                num = float(valor) if valor is not None else 0.0
                return "{:,.2f}".format(num).replace(",", "X").replace(".", ",").replace("X", ".")
            except:
                return "0,00"

        # Iterar sobre los resultados y llenar la tabla
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            row_position = self.table_productos.rowCount()
            self.table_productos.insertRow(row_position)

            # Cargar las columnas específicas
            self.table_productos.setItem(row_position, 0, QTableWidgetItem(str(row[0])))  # Código
            self.table_productos.setItem(row_position, 1, QTableWidgetItem(str(row[1])))  # Descripción
            self.table_productos.setItem(row_position, 2, QTableWidgetItem(str(row[2])))  # Marca
            # Verifica si la cantidad es None y asigna 0 si es necesario
            cantidad = row[3] if row[3] is not None else 0
            self.table_productos.setItem(row_position, 3, QTableWidgetItem(str(cantidad)))  # Existencia (cantidad)
            self.table_productos.setItem(row_position, 4, QTableWidgetItem(formato_monto(row[4])))  # Costo Actual
            self.table_productos.setItem(row_position, 5, QTableWidgetItem(formato_monto(row[5])))  # Costo Actual Referencial

        # Cierra la conexión a la base de datos
        conn.close()
    
    def recalcular_precios_bs_por_tasa(self, nueva_tasa):
        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Obtener todos los productos
        cursor.execute("""
            SELECT codigo, precio_sin_impuesto_dolar, precio_total_dolar, 
                costo_actual_referencial 
            FROM productos_inventario
        """)
        productos = cursor.fetchall()

        for producto in productos:
            codigo, precio_sin_impuesto_dolar, precio_total_dolar, costo_actual_referencial = producto

            # Recalcular los precios en bolívares usando la lógica de calcular_utilidad_y_impuesto
            precios_bs = self.calcular_precios_bs(
                float(round(precio_sin_impuesto_dolar, 4)),
                float(precio_total_dolar),
                float(costo_actual_referencial),
                nueva_tasa
            )

            # Actualizar los campos en la base de datos
            cursor.execute("""
                UPDATE productos_inventario 
                SET 
                    precio_sin_impuesto_bs = ?,
                    impuesto_total_bs = ?,
                    precio_total_bs = ?,
                    precio_sin_impuesto_bs_2 = ?,
                    impuesto_total_bs_2 = ?,
                    precio_total_bs_2 = ?,
                    precio_sin_impuesto_bs_3 = ?,
                    impuesto_total_bs_3 = ?,
                    precio_total_bs_3 = ?,
                    utilidad_bs = ?,
                    utilidad_bs_2 = ?,
                    utilidad_bs_3 = ?,
                    monto_utilidad_bs = ?,
                    monto_utilidad_bs_2 = ?,
                    monto_utilidad_bs_3 = ?
                WHERE codigo = ?
            """, (
                precios_bs['precio_sin_impuesto_bs'],
                precios_bs['impuesto_total_bs'],
                precios_bs['precio_total_bs'],
                precios_bs['precio_sin_impuesto_bs_2'],
                precios_bs['impuesto_total_bs_2'],
                precios_bs['precio_total_bs_2'],
                precios_bs['precio_sin_impuesto_bs_3'],
                precios_bs['impuesto_total_bs_3'],
                precios_bs['precio_total_bs_3'],
                precios_bs['utilidad_bs'],
                precios_bs['utilidad_bs_2'],
                precios_bs['utilidad_bs_3'],
                precios_bs['monto_utilidad_bs'],
                precios_bs['monto_utilidad_bs_2'],
                precios_bs['monto_utilidad_bs_3'],
                codigo
            ))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        # Actualizar la interfaz de usuario
        self.cargar_productos_en_tabla()

    def calcular_precios_bs(self, precio_sin_impuesto_dolar, precio_total_dolar, costo_actual_referencial, tasa):
        # Obtener el IVA desde la base de datos
        iva = self.obtener_tasa_impuesto()

        # Calcular precios en bolívares para la primera utilidad
        utilidad_dolar = (precio_sin_impuesto_dolar - costo_actual_referencial) / costo_actual_referencial
        costo_bs = costo_actual_referencial * tasa
        precio_sin_impuesto_bs = costo_bs * (1 + utilidad_dolar)
        impuesto_total_bs = precio_sin_impuesto_bs * iva
        precio_total_bs = precio_sin_impuesto_bs + impuesto_total_bs
        monto_utilidad_bs = costo_bs * utilidad_dolar

        # Calcular precios en bolívares para la segunda utilidad
        precio_sin_impuesto_bs_2 = precio_sin_impuesto_dolar * tasa
        impuesto_total_bs_2 = precio_sin_impuesto_bs_2 * iva
        precio_total_bs_2 = precio_sin_impuesto_bs_2 + impuesto_total_bs_2
        monto_utilidad_bs_2 = precio_sin_impuesto_bs_2 - costo_bs

        # Calcular precios en bolívares para la tercera utilidad
        precio_sin_impuesto_bs_3 = precio_sin_impuesto_dolar * tasa
        impuesto_total_bs_3 = precio_sin_impuesto_bs_3 * iva
        precio_total_bs_3 = precio_sin_impuesto_bs_3 + impuesto_total_bs_3
        monto_utilidad_bs_3 = precio_sin_impuesto_bs_3 - costo_bs

        # Redondear solo al final
        return {
            'precio_sin_impuesto_bs': precio_sin_impuesto_bs,
            'impuesto_total_bs': round(impuesto_total_bs, 4),
            'precio_total_bs': round(precio_total_bs, 2),
            'precio_sin_impuesto_bs_2': precio_sin_impuesto_bs_2,
            'impuesto_total_bs_2': impuesto_total_bs_2,
            'precio_total_bs_2': round(precio_total_bs_2, 2),
            'precio_sin_impuesto_bs_3': precio_sin_impuesto_bs_3,
            'impuesto_total_bs_3': impuesto_total_bs_3,
            'precio_total_bs_3': round(precio_total_bs_3, 2),
            'utilidad_bs': round(utilidad_dolar * 100, 4),
            'utilidad_bs_2': round(utilidad_dolar * 100, 4),
            'utilidad_bs_3': round(utilidad_dolar * 100, 4),
            'monto_utilidad_bs': round(monto_utilidad_bs, 4),
            'monto_utilidad_bs_2': round(monto_utilidad_bs_2, 4),
            'monto_utilidad_bs_3': round(monto_utilidad_bs_3, 4)
        }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = CrearProductos()
    MainWindow.show()
    sys.exit(app.exec_())