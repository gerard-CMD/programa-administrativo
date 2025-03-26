import sys
import json
import os
from PyQt5.QtWidgets import QGroupBox,QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QCheckBox, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QComboBox, QHeaderView, QAbstractItemView, QScrollArea, QFrame
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QMovie, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

class ConfiguracionPermisos(QDialog):
    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name

        self.setWindowTitle('ZISCON ADMINISTRATIVO (V 1.0)')
        self.setWindowIcon(QIcon('icono.png'))
        self.setStyleSheet("background-color: rgb(243, 252, 250);")
        self.setFixedSize(500, 460)

        # Layout principal
        main_layout = QVBoxLayout()

        # Crear marcos
        frame1 = QFrame(self)
        frame1.setFrameStyle(QFrame.StyledPanel)
        frame2 = QFrame(self)
        frame2.setFrameStyle(QFrame.StyledPanel)

        # Agregar atributos para almacenar los checkboxes
        self.checkboxes_acceso = []  # Lista para checkboxes de acceso
        self.checkboxes_permite = []  # Lista para checkboxes de permisos

        # Lista de acceso a módulo
        self.scroll_area_acceso = QScrollArea()
        self.scroll_area_acceso.setStyleSheet("""
            QScrollBar:vertical {
                background-color: rgb(243, 252, 250);
                width: 12px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #008080;
                border-radius: 5px;
                min-height: 1px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)  # Personalizar la barra de desplazamiento vertical
        self.scroll_widget_acceso = QWidget()
        self.scroll_layout_acceso = QVBoxLayout(self.scroll_widget_acceso)

        items_acceso = [
            "Marcas de Inventario",
            "Lineas de Inventario",
            "Depositos",
            "Productos",
            "Cargos de Productos",
            "Descargos de Productos",
            "Ajuste de Inventario",
            "Ajuste de Precios",
            "Monedas",
            "Formas de Pago",
            "Impuestos",
            "Tasa Cambiaria",
            "Proveedores",
            "Ordenes de Compra",
            "Compra de Mercancia",
            "Devolucion de Compra",
            "Cuentas por Pagar",
            "Cuentas por Cobrar",
            "Ordenes de Compra",
            "Presupuestos",
            "General",
            "Empresa",
            "Acerca de"
        ]

        for item in items_acceso:
            checkbox = QCheckBox(item)
            self.checkboxes_acceso.append(checkbox)  # Almacena el checkbox en la lista
            self.scroll_layout_acceso.addWidget(checkbox)

        self.scroll_widget_acceso.setLayout(self.scroll_layout_acceso)
        self.scroll_area_acceso.setWidget(self.scroll_widget_acceso)
        self.scroll_area_acceso.setWidgetResizable(True)

        # Lista de permisos
        self.scroll_area_permite = QScrollArea()
        self.scroll_widget_permite = QWidget()
        self.scroll_layout_permite = QVBoxLayout(self.scroll_widget_permite)

        items_permite = [
            "Incluye Registros",
            "Modifica Registros",
            "Elimina Registros",
            "Permite visualizar precios",
            "Permite visualizar costos",
            "Anulacion de documentos de ventas",
            "Anulacion de documentos de compras"
        ]

        for item in items_permite:
            checkbox = QCheckBox(item)
            self.checkboxes_permite.append(checkbox)  # Almacena el checkbox en la lista
            self.scroll_layout_permite.addWidget(checkbox)

        self.scroll_widget_permite.setLayout(self.scroll_layout_permite)
        self.scroll_area_permite.setWidget(self.scroll_widget_permite)
        self.scroll_area_permite.setWidgetResizable(True)

        # Etiquetas
        label_acceso = QLabel('ACCESO A MÓDULO:')
        label_permite = QLabel('PERMITE:')

        # Agregar elementos al marco 1
        layout1 = QVBoxLayout()
        layout1.addWidget(label_acceso)
        layout1.addWidget(self.scroll_area_acceso)
        frame1.setLayout(layout1)

        # Agregar elementos al marco 2
        layout2 = QVBoxLayout()
        layout2.addWidget(label_permite)
        layout2.addWidget(self.scroll_area_permite)
        frame2.setLayout(layout2)

        # Agregar marcos al layout principal
        h_layout = QHBoxLayout()
        h_layout.addWidget(frame1)
        h_layout.addWidget(frame2)

        main_layout.addLayout(h_layout)

        # Botón de Aceptar
        self.boton_aceptar = QPushButton('Aceptar')
        self.boton_aceptar.setStyleSheet("""
            QPushButton {
                background-color: #008080; 
                color: #fff; 
                border: none; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el botón */
            }
            QPushButton:pressed {
                background-color: #00698f; /* Color cuando se presiona el botón */
            }
            QPushButton:disabled {
                background-color: #ccc; /* Color cuando el botón está deshabilitado */
            }
        """)
        self.boton_aceptar.clicked.connect(self.guardar_permisos)  # Conectar el botón a la función
        main_layout.addWidget(self.boton_aceptar)

        self.setLayout(main_layout)

    def guardar_permisos(self):
        # Crear un diccionario de permisos
        permisos = {
            "acceso": {checkbox.text(): checkbox.isChecked() for checkbox in self.checkboxes_acceso},
            "permite": {checkbox.text(): checkbox.isChecked() for checkbox in self.checkboxes_permite}
        }
        
        # Cargar permisos existentes
        try:
            with open('permisos.json', 'r') as f:
                all_permisos = json.load(f)
        except FileNotFoundError:
            all_permisos = {}

        # Guardar permisos del usuario actual
        all_permisos[self.user_name] = permisos
        
        # Guardar todos los permisos de nuevo
        with open('permisos.json', 'w') as f:
            json.dump(all_permisos, f, indent=4)  # Usar indent=4 para mejor legibilidad
        
        self.accept()  # Cierra el diálogo

    def cargar_permisos(self):
        try:
            with open('permisos.json', 'r') as f:
                all_permisos = json.load(f)
                # Cargar permisos del usuario actual
                permisos = all_permisos.get(self.user_name, {})
                
                # Cargar permisos de acceso
                acceso_permisos = permisos.get("acceso", {})
                for checkbox in self.checkboxes_acceso:
                    # Verifica si el texto del checkbox está en los permisos de acceso
                    if checkbox.text() in acceso_permisos:
                        checkbox.setChecked(acceso_permisos[checkbox.text()])
                    else:
                        checkbox.setChecked(False)  # Si no está en el JSON, desmarcar

                # Cargar permisos adicionales
                permite_permisos = permisos.get("permite", {})
                for checkbox in self.checkboxes_permite:
                    # Verifica si el texto del checkbox está en los permisos adicionales
                    if checkbox.text() in permite_permisos:
                        checkbox.setChecked(permite_permisos[checkbox.text()])
                    else:
                        checkbox.setChecked(False)  # Si no está en el JSON, desmarcar

        except FileNotFoundError:
            print("El archivo permisos.json no se encontró.")

class Configuracion(QWidget):
    def __init__(self):
        super().__init__()
        self.default_currency = None  # Inicializa el atributo default_currency
        self.conn = sqlite3.connect("Usuarios.db")
        self.cursor = self.conn.cursor()
        self.is_editing = False  # Agrega esta línea
        self.code_exists = False  # Agrega esta variable a la clase

        self.factor_cambio_referencial = QLineEdit(self)
        self.factor_cambio_referencial.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.load_dolar_factor()  # Llama al método load_dolar_factor

        self.setWindowTitle("Configuración General")
        self.setFixedSize(1114, 710)
        self.setWindowIcon(QIcon("icono.png"))  # Agrega el icono a la ventana

        self.table_users = QTableWidget()
        self.load_users()  # Llama a load_users() aquí

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.crear_tab_principal(), "Principal")
        self.tab_widget.tabBar().setStyleSheet("""
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
        self.tab_widget.addTab(self.crear_tab_usuarios(), "Usuarios")

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

        # Crea el objeto moneda_local
        self.moneda_local = QComboBox()
        self.moneda_local.addItem("Seleccione una opción")
        self.cursor.execute("SELECT nombre FROM monedas")
        monedas = [row[0] for row in self.cursor.fetchall()]
        for moneda in monedas:
            self.moneda_local.addItem(moneda)

        # Lee la moneda por defecto desde la base de datos
        self.cursor.execute("SELECT moneda_por_defecto FROM sistema WHERE id = 1")
        default_currency = self.cursor.fetchone()[0]

        # Establecer la moneda por defecto como el valor seleccionado en el combobox
        index = self.moneda_local.findText(default_currency)
        if index != -1:
            self.moneda_local.setCurrentIndex(index)
        
        self.moneda_local.currentTextChanged.connect(self.load_moneda_info)
        self.moneda_local.currentTextChanged.connect(self.update_system_config)  # <--- Aquí va la conexión

        # Llama a load_moneda_info con el valor actual de moneda_local
        self.load_moneda_info(self.moneda_local.currentText())

    def crear_tab_principal(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Grupo de Moneda
        moneda_group = QGroupBox("Monedas")
        moneda_group.setGeometry(QtCore.QRect(0, 0, 200, 200))
        moneda_layout = QVBoxLayout()
        moneda_group.setStyleSheet("""
            QGroupBox {
                color: #000000;
                border: 1px solid #ccc; /* Borde del grupo */
                border-radius: 5px; /* Radio del borde del grupo */
                padding: 10px; /* Espacio entre el borde y el contenido */
            }
        """)

        # Crear un layout horizontal para los campos "Nombre Moneda" y "Símbolo"
        nombre_moneda_layout = QHBoxLayout()
        nombre_moneda_layout.addWidget(QLabel("Moneda:"))
        self.nombre_moneda = QLineEdit()
        self.nombre_moneda.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.nombre_moneda.setReadOnly(True)  # Establece el campo "Nombre Moneda" como de solo lectura
        self.nombre_moneda.setMaximumSize(150, 30)
        nombre_moneda_layout.addWidget(self.nombre_moneda)
        nombre_moneda_layout.addSpacing(260)
        nombre_moneda_layout.addWidget(QLabel("Símbolo:"))
        self.simbolo = QLineEdit()
        self.simbolo.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.simbolo.setReadOnly(True)  # Establece el campo "Símbolo" como de solo lectura
        self.simbolo.setMaximumSize(150, 30)
        self.simbolo.setFixedWidth(50)
        self.simbolo.setPlaceholderText("Bs.")
        nombre_moneda_layout.addWidget(self.simbolo)

        moneda_layout.addLayout(nombre_moneda_layout)

        # Cargar monedas desde la base de datos
        self.cursor.execute("SELECT nombre FROM monedas")
        monedas = [row[0] for row in self.cursor.fetchall()]

        # Crear campos de selección para Moneda Local, Factor de Cambio Referencial y Factor de Cambio Oficial
        self.moneda_local = QComboBox()
        self.moneda_local.addItem("")
        
        for moneda in monedas:
            self.moneda_local.addItem(moneda)

        # Agrega el estilo CSS aquí
        self.moneda_local.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::down-arrow {
                image: url(flechaa.png);
                width: 24px;
                height: 24px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::item:selected {
                background-color: #17a9a9; /* Fondo azul claro cuando se selecciona un item */
                color: #ffffff; /* Texto blanco cuando se selecciona un item */
            }
        """)
        # Leer la moneda por defecto desde la base de datos
        self.cursor.execute("SELECT moneda_por_defecto FROM sistema WHERE id = 1")
        default_currency = self.cursor.fetchone()[0]

        # Establecer la moneda por defecto como el valor seleccionado en el combobox
        index = self.moneda_local.findText(default_currency)
        if index != -1:
            self.moneda_local.setCurrentIndex(index)

        self.moneda_local.currentTextChanged.connect(self.load_moneda_info)
        self.moneda_local.currentTextChanged.connect(self.update_system_config)  # <--- Aquí va la conexión
        moneda_layout.addWidget(QLabel("Moneda Local"))
        moneda_layout.addWidget(self.moneda_local)

        moneda_layout.addWidget(QLabel("Factor de Cambio Referencial"))
        self.factor_cambio_referencial.setMaximumSize(150, 25)
        moneda_layout.addWidget(self.factor_cambio_referencial)

        moneda_group.setLayout(moneda_layout)

        # Grupo de Documentos
        documentos_group = QGroupBox("Documentos y Impuestos")
        documentos_group.setFixedSize(458, 200)
        documentos_layout = QVBoxLayout()
        documentos_group.setStyleSheet("""
            QGroupBox {
                color: #000000;
                border: 1px solid #ccc; /* Borde del grupo */
                border-radius: 5px; /* Radio del borde del grupo */
                padding: 10px; /* Espacio entre el borde y el contenido */
            }
        """)

        self.longitud_correlativos = QLineEdit()
        self.longitud_correlativos.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.longitud_correlativos.setMaximumSize(160, 30)
        self.longitud_correlativos.setFixedWidth(150)
        documentos_layout.addWidget(QLabel("Longitud de Los Correlativos"))
        documentos_layout.addWidget(self.longitud_correlativos)

        self.impuesto_defecto = QLineEdit()
        self.impuesto_defecto.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.impuesto_defecto.setMaximumSize(160, 30)
        self.impuesto_defecto.setFixedWidth(400)

        # Leer el primer impuesto desde la base de datos
        self.cursor.execute("SELECT * FROM impuestos ORDER BY id LIMIT 1")
        impuesto_default = self.cursor.fetchone()

        # Establecer el valor del impuesto por defecto como el primer impuesto creado
        if impuesto_default:
            self.impuesto_defecto.setText(impuesto_default[1])  # Asigna el nombre del impuesto
            self.impuesto_defecto.setReadOnly(True)
        else:
            self.impuesto_defecto.setPlaceholderText("No hay impuestos creados")

        documentos_layout.addWidget(QLabel("Impuesto por defecto"))
        documentos_layout.addWidget(self.impuesto_defecto)

        documentos_group.setLayout(documentos_layout)
        
        # Grupo de Impuestos POS
        impuestos_pos_group = QGroupBox("Impuestos POS")
        impuestos_pos_group.setFixedSize(605, 120)
        impuestos_pos_layout = QVBoxLayout()
        impuestos_pos_group.setStyleSheet("""
            QGroupBox {
                color: #000000;
                border: 1px solid #ccc; /* Borde del grupo */
                border-radius: 5px; /* Radio del borde del grupo */
                padding: 10px; /* Espacio entre el borde y el contenido */
            }
        """)

        impuesto1_layout = QHBoxLayout()
        impuesto1_layout.addWidget(QLabel("Impuesto 1"))
        self.impuesto1 = QLineEdit()
        self.impuesto1.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.impuesto1.setFixedWidth(150)
        impuesto1_layout.addWidget(self.impuesto1)
        impuesto1_layout.addWidget(QLabel("Porcentaje"))
        self.porcentaje1 = QLineEdit()
        self.porcentaje1.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.porcentaje1.setFixedWidth(150)
        impuesto1_layout.addWidget(self.porcentaje1)
        self.check_impuesto1 = QCheckBox("Activar Impuesto 1")
        self.check_impuesto1.setChecked(False)
        impuesto1_layout.addWidget(self.check_impuesto1)
        self.check_impuesto1.setStyleSheet("""
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

        impuestos_pos_layout.addLayout(impuesto1_layout)

        impuesto2_layout = QHBoxLayout()
        impuesto2_layout.addWidget(QLabel("Impuesto 1"))
        self.impuesto2 = QLineEdit()
        self.impuesto2.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.impuesto2.setFixedWidth(150)
        impuesto2_layout.addWidget(self.impuesto2)
        impuesto2_layout.addWidget(QLabel("Porcentaje"))
        self.porcentaje2 = QLineEdit()
        self.porcentaje2.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.porcentaje2.setFixedWidth(150)
        impuesto2_layout.addWidget(self.porcentaje2)
        self.check_impuesto2 = QCheckBox("Activar Impuesto 1")
        self.check_impuesto2.setChecked(False)
        impuesto2_layout.addWidget(self.check_impuesto2)
        self.check_impuesto2.setStyleSheet("""
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

        impuestos_pos_layout.addLayout(impuesto2_layout)

        impuestos_pos_group.setLayout(impuestos_pos_layout)

        # Grupo adicional
        adicional_group = QGroupBox("Adicional")
        adicional_group.setFixedSize(605, 260)
        adicional_layout = QVBoxLayout()
        adicional_group.setStyleSheet("""
            QGroupBox {
                color: #000000;
                border: 1px solid #ccc; /* Borde del grupo */
                border-radius: 5px; /* Radio del borde del grupo */
                padding: 10px; /* Espacio entre el borde y el contenido */
            }
        """)

        # Agrega un QLabel y un QComboBox para los decimales generales
        self.label_decimals_general = QLabel("Decimales generales:")
        self.decimals_general = QComboBox()
        self.decimals_general.addItem("2")
        self.decimals_general.addItem("3")
        self.decimals_general.addItem("4")
        self.decimals_general.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::drop-down {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::down-arrow {
                image: url(flechaa.png);
                width: 24px;
                height: 24px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
        """)
        self.decimals_general.setCurrentIndex(0) # Establece el valor predeterminado en 2 decimales
        self.decimals_general.currentTextChanged.connect(lambda decimals: self.update_decimals("general", decimals))

        # Agrega un QLabel y un QComboBox para los decimales de cantidades
        self.label_decimals_cantidades = QLabel("Decimales de cantidades:")
        self.decimals_cantidades = QComboBox()
        self.decimals_cantidades.addItem("2")
        self.decimals_cantidades.addItem("3")
        self.decimals_cantidades.addItem("4")
        self.decimals_cantidades.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::drop-down {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::down-arrow {
                image: url(flechaa.png);
                width: 24px;
                height: 24px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
        """)
        self.decimals_cantidades.setCurrentIndex(0) # Establece el valor predeterminado en 2 decimales
        self.decimals_cantidades.currentTextChanged.connect(lambda decimals: self.update_decimals("cantidades", decimals))

        # Agrega un QLabel y un QComboBox para los decimales de retenciones
        self.label_decimals_retenciones = QLabel("Decimales de retenciones:")
        self.decimals_retenciones = QComboBox()
        self.decimals_retenciones.addItem("2")
        self.decimals_retenciones.addItem("3")
        self.decimals_retenciones.addItem("4")
        self.decimals_retenciones.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::drop-down {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::down-arrow {
                image: url(flechaa.png);
                width: 24px;
                height: 24px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
        """)
        self.decimals_retenciones.setCurrentIndex(0) # Establece el valor predeterminado en 2 decimales
        self.decimals_retenciones.currentTextChanged.connect(lambda decimals: self.update_decimals("retenciones", decimals))

        self.tipo_costo_u = QComboBox()
        self.tipo_costo_u.addItem("Seleccione una opción")
        self.tipo_costo_u.addItem("Costo Actual")
        self.tipo_costo_u.addItem("Costo Promedio")
        self.tipo_costo_u.addItem("Costo Anterior")
        self.tipo_costo_u.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::drop-down {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::down-arrow {
                image: url(flechaa.png);
                width: 24px;
                height: 24px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
        """)

        # Agrega un QCheckBox para convertir a moneda local al incluir precios en moneda referencial
        self.check_moneda_referencial = QCheckBox("Convertir a moneda local al incluir precios en moneda referencial")
        self.check_moneda_referencial.setStyleSheet("""
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
        self.check_moneda_referencial.stateChanged.connect(self.on_check_state_changed)

        # Agrega los widgets al layout
        adicional_layout.addWidget(QLabel("Tipo de Costo Utilidad"))
        adicional_layout.addWidget(self.tipo_costo_u)
        adicional_layout.addWidget(self.label_decimals_general)
        adicional_layout.addWidget(self.decimals_general)
        adicional_layout.addWidget(self.label_decimals_cantidades)
        adicional_layout.addWidget(self.decimals_cantidades)
        adicional_layout.addWidget(self.label_decimals_retenciones)
        adicional_layout.addWidget(self.decimals_retenciones)
        adicional_layout.addWidget(self.check_moneda_referencial)

        # Agrega el layout al grupo adicional
        adicional_group.setLayout(adicional_layout)

        self.imagen_configuracion= QLabel(self)
        pixmap = QPixmap("config.png")
        self.imagen_configuracion.setPixmap(pixmap)
        self.imagen_configuracion.setGeometry(QtCore.QRect(600, 230, 750, 500))

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addWidget(moneda_group)
        main_layout.addWidget(documentos_group)

        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(impuestos_pos_group)
        bottom_layout.addWidget(adicional_group)

        # Layout horizontal para incluir la imagen
        image_layout = QHBoxLayout()
        image_layout.addLayout(bottom_layout)
        image_layout.addSpacing(100)
        image_layout.addWidget(self.imagen_configuracion)

        layout.addLayout(main_layout)
        layout.addLayout(image_layout)

        tab.setLayout(layout)

        self.load_decimals()
        
        return tab

    def on_check_state_changed(self, state):
        if state == Qt.Checked:
            # Obtén el valor del factor de cambio referencial desde la interfaz de usuario
            factor_cambio_referencial = float(self.factor_cambio_referencial.text())

            # Obtén los precios en moneda referencial desde la interfaz de usuario o desde otra fuente de datos
            precio_referencial_1 = 100
            precio_referencial_2 = 200

            # Realiza la conversión de moneda
            precio_convertido_1 = precio_referencial_1 * factor_cambio_referencial
            precio_convertido_2 = precio_referencial_2 * factor_cambio_referencial

            # Actualiza los precios en moneda local en la interfaz de usuario
            #self.line_edit_precio_1.setText(str(precio_convertido_1))
            #self.line_edit_precio_2.setText(str(precio_convertido_2))

            print("Checkbox activado. Convirtiendo a moneda local...")
        else:
            print("Checkbox desactivado.")

    def update_decimals(self, decimals_type, decimals):
        if decimals_type == "general":
            column = "decimals_general"
        elif decimals_type == "cantidades":
            column = "decimals_cantidades"
        elif decimals_type == "retenciones":
            column = "decimals_retenciones"
        else:
            raise ValueError(f"Invalid decimals type: {decimals_type}")
        self.cursor.execute("UPDATE sistema SET {column} = ? WHERE id = 1".format(column=column), (decimals,))
        self.conn.commit()
        print("Número de decimales actualizado correctamente en la tabla sistema")

    def load_decimals(self):
        self.cursor.execute("SELECT decimals_general, decimals_cantidades, decimals_retenciones FROM sistema WHERE id = 1")
        row = self.cursor.fetchone()
        if row:
            self.decimals_general.setCurrentIndex(self.decimals_general.findText(str(row[0])))
            self.decimals_cantidades.setCurrentIndex(self.decimals_cantidades.findText(str(row[1])))
            self.decimals_retenciones.setCurrentIndex(self.decimals_retenciones.findText(str(row[2])))
            print("Decimals cargados correctamente desde la base de datos")
        else:
            print("No se encontraron decimals configurados en la base de datos")

    def set_default_currency(self, currency):
        # Actualiza la configuración del sistema con la nueva moneda seleccionada
        self.default_currency = currency
        self.update_system_config()

    def update_system_config(self):
        self.cursor.execute("UPDATE sistema SET moneda_por_defecto = ? WHERE id = 1", (self.default_currency,))
        self.conn.commit()
        print("Moneda actualizada correctamente en la tabla sistema")

    def load_moneda_info(self, moneda):
        self.cursor.execute("SELECT nombre, simbolo FROM monedas WHERE nombre = ?", (moneda,))
        row = self.cursor.fetchone()
        if row:
            self.nombre_moneda.setText(row[0])  # Asigna el nombre de la moneda
            self.simbolo.setText(row[1])  # Asigna el símbolo de la moneda
            # Actualiza las columnas moneda_nombre y moneda_simbolo en la tabla sistema
            self.cursor.execute("UPDATE sistema SET moneda_nombre = ?, moneda_simbolo = ? WHERE id = 1", (row[0], row[1]))
            self.conn.commit()
            self.default_currency = moneda  # Update default_currency with the selected moneda

    def load_dolar_factor(self):
        self.cursor.execute("SELECT factor_inventario FROM monedas WHERE nombre = 'Dolares'")
        row = self.cursor.fetchone()
        if row:
            self.factor_cambio_referencial.setText(str(row[0]))  # Asigna el valor del factor de cambio referencial
            self.factor_cambio_referencial.setReadOnly(True)  # Establece el campo como de solo lectura

    def crear_tab_usuarios(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.imagen_cargos= QLabel(self)
        pixmap = QPixmap("z_usuarios.png")
        self.imagen_cargos.setPixmap(pixmap)
        self.imagen_cargos.show()
        
        # Campos de entrada
        self.label_code = QLabel("Código:")
        self.edit_code = QLineEdit()
        self.edit_code.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.label_description = QLabel("Descripción:")
        self.edit_description = QLineEdit()
        self.edit_description.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.label_user = QLabel("Usuario:")
        self.edit_user = QLineEdit()
        self.edit_user.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.label_password = QLabel("Clave:")
        self.edit_password = QLineEdit()
        self.edit_password.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.label_level = QLabel("Nivel:")
        self.combo_level = QComboBox()
        self.combo_level.addItems(["Master"])
        self.combo_level.addItems(["Directiva"])
        self.combo_level.addItems(["Administración"])
        self.combo_level.addItems(["Ventas"])
        self.check_active = QCheckBox("Activo")
        self.check_active.setMaximumWidth(70)  # Establece el ancho máximo en 100 píxeles
        self.check_active.setStyleSheet("""
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

        self.combo_level.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::down-arrow {
                image: url(flechaa.png);
                width: 24px;
                height: 24px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::item:selected {
                background-color: #17a9a9; /* Fondo azul claro cuando se selecciona un item */
                color: #ffffff; /* Texto blanco cuando se selecciona un item */
            }
        """)

        self.edit_code.setEnabled(False)
        self.edit_description.setEnabled(False)
        self.edit_user.setEnabled(False)
        self.edit_password.setEnabled(False)
        self.combo_level.setEnabled(False)
        self.check_active.setEnabled(False)

        # Botones
        self.button_roles = QPushButton("Permisos")
        self.button_roles.setMaximumWidth(100)  # Establece el ancho máximo en 100 píxeles
        self.button_roles.setStyleSheet("""
            QPushButton {
                background-color: #008080; 
                color: #fff; 
                border: none; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el botón */
            }
            QPushButton:pressed {
                background-color: #00698f; /* Color cuando se presiona el botón */
            }
            QPushButton:disabled {
                background-color: #ccc; /* Color cuando el botón está deshabilitado */
            }
        """)

        self.button_roles.clicked.connect(self.show_permisos)
        self.button_roles.setEnabled(False)

        self.button_add = QPushButton("Añadir usuario")
        self.button_add.setMaximumWidth(100)  # Establece el ancho máximo en 100 píxeles
        self.button_add.setStyleSheet("""
            QPushButton {
                background-color: #008080; 
                color: #fff; 
                border: none; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el botón */
            }
            QPushButton:pressed {
                background-color: #00698f; /* Color cuando se presiona el botón */
            }
            QPushButton:disabled {
                background-color: #ccc; /* Color cuando el botón está deshabilitado */
            }
        """)
        self.button_add.clicked.connect(self.add_user)

        self.button_modify = QPushButton("Modificar")
        self.button_modify.setMaximumWidth(100)  # Establece el ancho máximo en 100 píxeles
        self.button_modify.setStyleSheet("""
            QPushButton {
                background-color: #008080; 
                color: #fff; 
                border: none; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el botón */
            }
            QPushButton:pressed {
                background-color: #00698f; /* Color cuando se presiona el botón */
            }
            QPushButton:disabled {
                background-color: #ccc; /* Color cuando el botón está deshabilitado */
            }
        """)
        self.button_modify.clicked.connect(self.modify_user)
        self.button_modify.setEnabled(False)

        self.button_delete = QPushButton("Eliminar")
        self.button_delete.setMaximumWidth(100)  # Establece el ancho máximo en 100 píxeles
        self.button_delete.setStyleSheet("""
            QPushButton {
                background-color: #008080; 
                color: #fff; 
                border: none; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el botón */
            }
            QPushButton:pressed {
                background-color: #00698f; /* Color cuando se presiona el botón */
            }
            QPushButton:disabled {
                background-color: #ccc; /* Color cuando el botón está deshabilitado */
            }
        """)
        self.button_delete.clicked.connect(self.delete_user)
        self.button_delete.setEnabled(False)

        self.button_cancel = QPushButton("Cancelar")
        self.button_cancel.setMaximumWidth(100)  # Establece el ancho máximo en 100 píxeles
        self.button_cancel.setStyleSheet("""
            QPushButton {
                background-color: #008080; 
                color: #fff; 
                border: none; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el botón */
            }
            QPushButton:pressed {
                background-color: #00698f; /* Color cuando se presiona el botón */
            }
            QPushButton:disabled {
                background-color: #ccc; /* Color cuando el botón está deshabilitado */
            }
        """)
        self.button_cancel.clicked.connect(self.cancel_user)
        self.button_cancel.setEnabled(False)  # Deshabilita el botón cancelar por defecto

        # Tabla de usuarios
        self.table_users = QTableWidget()
        self.table_users.setColumnCount(2)
        self.table_users.setHorizontalHeaderLabels(["Código", "Descripción"])
        self.table_users.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_users.verticalHeader().setVisible(False)
        self.table_users.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_users.setStyleSheet("QTableWidget::item:selected {\n"
        "                background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */\n"
        "                color: white; /* Color del texto de la fila seleccionada */\n"
        "            }\n"
        "            QHeaderView::section {\n"
        "                background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */\n"
        "                border: 5px;\n"
        "                color: #ffffff;\n"
        "            }")
        self.table_users.itemSelectionChanged.connect(self.load_user_data)
        self.table_users.itemSelectionChanged.connect(self.itemSelectionChanged)

        # Campos de entrada
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.imagen_cargos)
        input_layout.addWidget(self.label_code)
        input_layout.addWidget(self.edit_code)
        input_layout.addWidget(self.label_description)
        input_layout.addWidget(self.edit_description)
        input_layout.addWidget(self.label_user)
        input_layout.addWidget(self.edit_user)
        input_layout.addWidget(self.label_password)
        input_layout.addWidget(self.edit_password)
        input_layout.addWidget(self.label_level)
        input_layout.addWidget(self.combo_level)
        input_layout.addWidget(self.check_active)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_add)
        button_layout.addWidget(self.button_roles)
        button_layout.addWidget(self.button_modify)
        button_layout.addWidget(self.button_delete)
        button_layout.addWidget(self.button_cancel)

        # Layout que contiene los campos de texto y botones
        right_layout = QVBoxLayout()
        right_layout.addLayout(input_layout)
        right_layout.addLayout(button_layout)

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.table_users)
        main_layout.addLayout(right_layout)

        # Inicialización de la tabla de usuarios
        self.load_users()

        tab.setLayout(main_layout)  # Asigna el layout principal a la pestaña
        
        return tab
    
    def enable_fields(self):
        self.table_users.setEnabled(False)
        self.edit_code.setEnabled(True)
        self.edit_description.setEnabled(True)
        self.edit_user.setEnabled(True)
        self.edit_password.setEnabled(True)
        self.combo_level.setEnabled(True)
        self.check_active.setEnabled(True)

        self.button_roles.setEnabled(True)
        self.button_cancel.setEnabled(True)  # Habilita el botón cancelar

    def disable_fields(self):
        self.edit_code.setEnabled(False)
        self.edit_description.setEnabled(False)
        self.edit_user.setEnabled(False)
        self.edit_password.setEnabled(False)
        self.combo_level.setEnabled(False)
        self.check_active.setEnabled(False)
        
    def show_permisos(self):
        permisos = ConfiguracionPermisos(self.edit_user.text())  # Pasa el nombre del usuario actual
        permisos.cargar_permisos()
        permisos.exec_()

    def load_users(self):
        self.conn = sqlite3.connect("Usuarios.db")
        self.cursor = self.conn.cursor()

        # Limpia la tabla de usuarios
        self.table_users.setRowCount(0)

        # Lee los usuarios de la base de datos
        self.cursor.execute("SELECT * FROM usuarios")
        rows = self.cursor.fetchall()

        # Agrega los usuarios a la tabla
        for row in rows:
            row_count = self.table_users.rowCount()
            self.table_users.insertRow(row_count)
            self.table_users.setItem(row_count, 0, QTableWidgetItem(str(row[0])))  # Código
            self.table_users.setItem(row_count, 1, QTableWidgetItem(row[1]))  # Descripción

    def cancel_user(self):
        self.clear_fields()
        self.table_users.setEnabled(True)
        self.button_add.setEnabled(True)
        self.button_roles.setEnabled(False)
        self.button_modify.setEnabled(False)
        self.button_delete.setEnabled(False)
        self.button_cancel.setEnabled(False)  # Deshabilita el botón cancelar

        self.table_users.setRowCount(0)
        self.load_users()

        self.is_editing = False  # Establece en False para indicar que no se está editando

        # Deshabilita los campos de entrada
        self.edit_code.setEnabled(False)
        self.edit_description.setEnabled(False)
        self.edit_user.setEnabled(False)
        self.edit_password.setEnabled(False)
        self.combo_level.setEnabled(False)
        self.check_active.setEnabled(False)

        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect()  # Desconectar la señal de actualización
        self.button_modify.clicked.connect(self.modify_user)

        self.button_add.setText("Añadir Impuesto")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_user)

    def add_user(self):
        self.is_editing = False
        self.table_users.setEnabled(False)
        self.enable_fields()
        self.button_add.setText("Guardar cambios")
        self.button_add.clicked.disconnect(self.add_user)
        self.button_add.clicked.connect(self.guardar_nuevo_usuario)
    
    def guardar_nuevo_usuario(self):
        self.conn = sqlite3.connect("Usuarios.db")
        self.cursor = self.conn.cursor()
        
        self.edit_code.setEnabled(True)
        self.edit_description.setEnabled(True)
        self.edit_user.setEnabled(True)
        self.edit_password.setEnabled(True)
        self.combo_level.setEnabled(True)
        self.check_active.setEnabled(True)

        # Obtiene los datos del formulario
        code = self.edit_code.text()
        description = self.edit_description.text()
        user = self.edit_user.text()
        password = self.edit_password.text()
        level = self.combo_level.currentText()
        active = self.check_active.isChecked()

        # Verifica si estás editando un usuario existente
        if not self.is_editing:
            # Verifica si el código ya existe en la base de datos
            self.cursor.execute("SELECT 1 FROM usuarios WHERE codigo = ?", (code,))
            if self.cursor.fetchone():
                QMessageBox.warning(self, "Error", "El código ya existe. Por favor, ingrese un código único.")
                return
            # Inserta los datos del usuario en la tabla usuarios
            self.cursor.execute("INSERT INTO usuarios (codigo, descripcion, usuario, clave, nivel, activo) VALUES (?, ?, ?, ?, ?, ?)",
                                (code, description, user, password, level, active))
            # Guarda los cambios
            self.conn.commit()
            # Agrega una nueva fila a la tabla de usuarios
            row_count = self.table_users.rowCount()
            self.table_users.insertRow(row_count)
            self.table_users.setItem(row_count, 0, QTableWidgetItem(code))
            self.table_users.setItem(row_count, 1, QTableWidgetItem(description))

            # Limpia los campos del formulario
            self.clear_form()
            self.table_users.setEnabled(True)
            self.disable_fields()
            self.button_add.setText("Añadir usuario")
            self.button_add.clicked.disconnect(self.guardar_nuevo_usuario)
            self.button_add.clicked.connect(self.add_user)

        # Cierra la conexión a la base de datos
        self.conn.close()

    def modify_user(self):
        self.table_users.setEnabled(False)
        row = self.table_users.currentRow()
        if row != -1:
            self.enable_fields()
            self.button_modify.setText("Guardar cambios")
            self.button_modify.clicked.disconnect(self.modify_user)  
            self.button_modify.clicked.connect(self.update_user)

        # Habilita el botón de roles si hay un código
        self.button_roles.setEnabled(bool(self.edit_code.text()))

        # Carga la información del usuario seleccionado
        self.load_user_data()
        self.button_roles.setEnabled(True)
        self.button_cancel.setEnabled(True)  # Habilita el botón cancelar

        # Habilita los campos de texto, excepto el código
        self.table_users.setEnabled(False)
        self.edit_description.setEnabled(True)
        self.edit_user.setEnabled(True)
        self.edit_password.setEnabled(True)
        self.combo_level.setEnabled(True)
        self.check_active.setEnabled(True)

    def update_user(self):
        self.conn = sqlite3.connect("Usuarios.db")
        self.cursor = self.conn.cursor()

        # Obtiene la información del usuario seleccionado
        selected_row = self.table_users.currentRow()
        if selected_row == -1:
            return

        # Obtiene el código del usuario seleccionado
        user_code = self.table_users.item(selected_row, 0).text()

        # Actualiza la información del usuario en la base de datos
        description = self.edit_description.text()
        username = self.edit_user.text()
        password = self.edit_password.text()
        # Verificar si la contraseña es diferente a la actual
        self.cursor.execute("SELECT clave FROM usuarios WHERE codigo = ?", (user_code,))
        current_password = self.cursor.fetchone()[0]
        if password != current_password:
            # Si la contraseña es diferente, actualiza la contraseña en la base de datos
            self.cursor.execute("UPDATE usuarios SET clave = ? WHERE codigo = ?", (password, user_code))
        else:
            # Si la contraseña es la misma, no se hace nada
            pass

        level = self.combo_level.currentText()
        active = self.check_active.isChecked()

        self.cursor.execute("UPDATE usuarios SET descripcion = ?, usuario = ?, clave = ?, nivel = ?, activo = ? WHERE codigo = ?",
                            (description, username, password, level, active, user_code))
        self.conn.commit()

        # Actualiza la tabla de usuarios
        self.load_users()
        self.table_users.setEnabled(True)
        self.disable_fields()
        
        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect(self.update_user)  # Desconectar la señal de actualización
        self.button_modify.clicked.connect(self.modify_user)

        # Cierra la conexión a la base de datos
        self.conn.close()

    def delete_user(self):
        # Obtiene el usuario seleccionado
        selected_row = self.table_users.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Por favor, seleccione un usuario.")
            return

        # Verifica si la fila seleccionada es válida
        if not self.table_users.item(selected_row, 0):
            QMessageBox.warning(self, "Error", "No se ha seleccionado un usuario válido.")
            return

        # Confirma la eliminación
        if QMessageBox.question(self, "Confirmar eliminación", "¿Está seguro de eliminar este usuario?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            # Guarda el código del usuario seleccionado
            user_code = self.table_users.item(selected_row, 0).text()

            # Elimina la fila de la tabla de usuarios
            self.table_users.removeRow(selected_row)

            # Conecta a la base de datos
            self.conn = sqlite3.connect("Usuarios.db")
            self.cursor = self.conn.cursor()

            # Elimina el usuario de la base de datos
            self.cursor.execute("DELETE FROM usuarios WHERE codigo = ?", (user_code,))

            # Guarda los cambios
            self.conn.commit()

            # Cierra la conexión a la base de datos
            self.conn.close()

        # Actualiza la selección de la tabla de usuarios
        self.table_users.setCurrentCell(-1, 0)

        # Actualiza la tabla de usuarios
        self.load_users()

        self.clear_form()
        self.button_delete.setEnabled(False)

    def close(self):
        self.conn.close()
        super().close()

    def load_user_data(self):
        self.conn = sqlite3.connect("Usuarios.db")
        self.cursor = self.conn.cursor()

        # Obtiene el usuario seleccionado
        selected_row = self.table_users.currentRow()
        if selected_row == -1:
            self.clear_fields()
            self.button_modify.setEnabled(False)
            self.button_delete.setEnabled(False)
            self.button_roles.setEnabled(False)  # Deshabilita el botón de roles
            return

        self.code_exists = True

        # Carga los datos del usuario en el formulario
        user = self.table_users.item(selected_row, 0).text()  # Código
        self.cursor.execute("SELECT * FROM usuarios WHERE codigo = ?", (user,))
        row = self.cursor.fetchone()
        if row:
            self.edit_code.setText(str(row[0]))  # Código
            self.edit_description.setText(row[1])  # Descripción
            self.edit_user.setText(row[2])  # Username
            self.edit_password.setText(str(row[3])) # Clave (no se muestra la clave actual)
            self.combo_level.setCurrentText(str(row[4]))  # Nivel
            self.check_active.setChecked(row[5] == 1)  # Activo

            # Deshabilita los campos de texto
            self.edit_code.setEnabled(False)
            self.edit_description.setEnabled(False)
            self.edit_user.setEnabled(False)
            self.edit_password.setEnabled(False)
            self.combo_level.setEnabled(False)
            self.check_active.setEnabled(False)

        # Cierra la conexión a la base de datos
        self.conn.close()

        if not self.table_users.selectedItems():
            self.clear_fields()
            
        self.button_modify.setEnabled(True)
        self.button_delete.setEnabled(True)

    def clear_form(self):
        # Limpia los campos del formulario
        self.edit_code.clear()
        self.edit_description.clear()
        self.edit_user.clear()
        self.edit_password.clear()
        self.combo_level.setCurrentIndex(0)
        self.check_active.setChecked(False)
        self.code_exists = False

        # Deshabilita los botones
        self.button_modify.setEnabled(False)
        self.button_delete.setEnabled(False)

    def clear_fields(self):
        self.edit_code.clear()
        self.edit_description.clear()
        self.edit_user.clear()
        self.edit_password.clear()
        self.combo_level.setCurrentIndex(0) # Restablece el índice del combo box
        self.check_active.setChecked(False)

        # Deshabilita los botones
        self.button_modify.setEnabled(False)
        self.button_delete.setEnabled(False)

    def itemSelectionChanged(self):
        if not self.table_users.selectedItems():
            self.button_add.setEnabled(True)
            self.button_modify.setEnabled(False)
            self.button_delete.setEnabled(False)
            self.button_roles.setEnabled(False)
            self.button_cancel.setEnabled(False)  # Deshabilita el botón de roles
        else:
            self.button_add.setEnabled(False)
            self.button_modify.setEnabled(True)
            self.button_delete.setEnabled(True)
            self.button_cancel.setEnabled(True)
        

    def cancel(self):
        # Habilita los campos de texto
        self.enable_fields()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = Configuracion()
    config.load_decimals()
    config.show()
    sys.exit(app.exec_())