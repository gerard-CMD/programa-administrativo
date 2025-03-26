import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QMainWindow, QMenu, QMenuBar, QAction, QStatusBar, QLabel, QStackedWidget, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer,QDateTime, Qt
from utils import MainApplication
from Login_Window import LoginWindow
from Configuracion_Monedas import Monedas  # Importar la ventana de monedas
from Formas_Pago import FormasDePago
from Configuracion_General import Configuracion
from Configuracion_Impuestos import ConfiguracionImpuestos
from Configuracion_Depositos import ConfiguracionDepositos
from Crear_Marcas import ConfiguracionMarcas
from Linea_Inventario import ConfiguracionLinea
from Crear_Productos import CrearProductos
from CARGAR_PRODUCTOS import CargarProductos
from DESCARGAR_PRODUCTOS import DescargarProductos
from AJUSTE_PRODUCTOS import AjusteProductos
from proveedores import Proveedores
from info_empresa import InformacionEmpresa
from tasa_c import MainWindow
from acerca_de import AboutDialog
from editor import Editor
import sqlite3

class MainApplication(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.username = login_window.username_input.text()
        self.conn = sqlite3.connect('Usuarios.db')  # nombre de tu base de datos
        self.cursor = self.conn.cursor()
        self.rol = self.get_rol()

        self.setWindowTitle("ZISCON ADMINISTRATIVO (V 1.0)")
        self.setFixedSize(1114, 710)
        self.setWindowIcon(QIcon("icono.png"))  # Agrega el icono a la ventana
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        

        # Crea un layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        self.layout_principal.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes del layout
        self.layout_principal.setSpacing(0)  # Elimina el espacio entre los elementos del layout
        self.central_widget.setLayout(self.layout_principal)

        # Crea un QStackedWidget para manejar las diferentes "ventanas"
        self.stacked_widget = QStackedWidget(self)
        self.layout_principal.addWidget(self.stacked_widget)

        # Crea un widget para la imagen de fondo
        self.image_widget = QWidget()
        self.image_layout = QVBoxLayout(self.image_widget)
        self.image_label = QLabel(self)
        self.image_label.setStyleSheet("background-image: url('fondo2.png'); background-repeat: no-repeat; background-position: center;")
        self.image_label.setScaledContents(True)  # Agrega esta línea
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_layout.addWidget(self.image_label)
        self.stacked_widget.addWidget(self.image_widget)

        # Crea instancias de las diferentes "ventanas" y añádelas al QStackedWidget
        self.monedas_widget = Monedas()
        self.impuestos_widget = ConfiguracionImpuestos()
        self.linea_widget = ConfiguracionLinea()
        self.crear_productos_widget = CrearProductos()
        self.cargar_productos_widget = CargarProductos()
        self.descargar_productos_widget = DescargarProductos()
        self.ajuste_productos_widget = AjusteProductos()
        self.crear_marcas_widget = ConfiguracionMarcas()
        self.configuracion_depositos_widget = ConfiguracionDepositos()
        self.formas_pago_widget = FormasDePago()
        self.configuracion_general_widget = Configuracion()
        self.tasa_c_widget = MainWindow()
        self.proveedores_widget = Proveedores()

        # Agregar widgets al QStackedWidget
        self.stacked_widget.addWidget(self.monedas_widget)
        self.stacked_widget.addWidget(self.linea_widget)
        self.stacked_widget.addWidget(self.impuestos_widget)
        self.stacked_widget.addWidget(self.crear_productos_widget)
        self.stacked_widget.addWidget(self.cargar_productos_widget)
        self.stacked_widget.addWidget(self.descargar_productos_widget)
        self.stacked_widget.addWidget(self.ajuste_productos_widget)
        self.stacked_widget.addWidget(self.crear_marcas_widget)
        self.stacked_widget.addWidget(self.configuracion_depositos_widget)
        self.stacked_widget.addWidget(self.formas_pago_widget)
        self.stacked_widget.addWidget(self.configuracion_general_widget)
        self.stacked_widget.addWidget(self.tasa_c_widget)
        self.stacked_widget.addWidget(self.proveedores_widget)

        # Crea la barra de menú
        self.barra_menus1 = QMenuBar(self)
        self.setMenuBar(self.barra_menus1)
        self.barra_menus1.setStyleSheet("""
            QMenuBar {
                background-color: #47a2a2;
                color: #000000;
            }
            QMenuBar::item {
                background-color: #47a2a2;
                color: #fff;
            }
            QMenuBar::item:selected {
                background-color: #1bb0b0;
                color: #ffffff;
            }
            QMenuBar::item:pressed {
                background-color: #1bb0b0;
                color: #ffffff;
            }
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #008080;
                color: #ffffff;
            }
            QMenu::item:pressed {
                background-color: #008080;
                color: #ffffff;
            }
            QMenu::item:hover {
                background-color: #1bb0b0;
                color: #ffffff;
            }
            QSubMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QSubMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QSubMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
            QSubMenu::item:pressed {
                background-color: #1bb0b0;
                color: #ffffff;
            }
            QSubMenu::item:hover {
                background-color: #1bb0b0;
                color: #ffffff;
            }
            QToolBar {
                background-color: #1bb0b0;
                color: #000000;
            }
            QToolBar::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QToolBar::item:selected {
                background-color: #1bb0b0;
                color: #ffffff;
            }
            QToolBar::item:pressed {
                background-color: #1bb0b0;
                color: #ffffff;
            }
            QToolBar::item:hover {
                background-color: #1ABC9C;
                color: #ffffff;
            }
        """)
        
        self.menu5 = QMenu("Inicio", self)
        self.barra_menus1.addMenu(self.menu5)

        # Crea una acción para mostrar la imagen de fondo
        icon = QIcon()
        icon.addFile("inicio_icon.png")
        self.action_show_image = QAction("inicio", self)
        self.action_show_image.setIcon(icon)  # Establece el icono para la acción
        self.action_show_image.triggered.connect(self.show_image)  # Conecta la acción a la función show_image
        self.menu5.addAction(self.action_show_image)
        self.menu5.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)
        
        self.menu = QMenu("Archivo", self)
        self.barra_menus1.addMenu(self.menu)

        # Crear la acción para abrir el editor
        open_editor_action = QAction("Abrir Editor (Ctrl+E)", self)
        open_editor_action.setShortcut("Ctrl+E")
        open_editor_action.triggered.connect(self.open_editor)

        # Agregar la acción a la barra de menú
        self.addAction(open_editor_action)

        icon = QIcon()
        icon.addFile("marcas.png")
        self.action_marcas = QAction("Marcas de inventario", self)
        self.action_marcas.setIcon(icon)  # Establece el icono para la acción
        self.action_marcas.triggered.connect(lambda: self.acceder_modulo("Marcas de Inventario"))
        self.menu.addAction(self.action_marcas)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)

        icon = QIcon()
        icon.addFile("linea.png")
        self.action_linea = QAction("Lineas de inventario", self)
        self.action_linea.setIcon(icon)  # Establece el icono para la acción
        self.action_linea.triggered.connect(lambda: self.acceder_modulo("Lineas de Inventario"))
        self.menu.addAction(self.action_linea)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)

        icon = QIcon()
        icon.addFile("archivo_icon.png")
        self.action_depositos = QAction("Depositos", self)
        self.action_depositos.setIcon(icon)  # Establece el icono para la acción
        self.action_depositos.triggered.connect(lambda: self.acceder_modulo("Depositos"))
        self.menu.addAction(self.action_depositos)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)

        self.menu5.addSeparator()  # Agrega un separador entre las acciones

        icon = QIcon()
        icon.addFile("salir_icon.png")
        self.action_salir = QAction("Salir", self)
        self.action_salir.setIcon(icon)  # Establece el icono para la acción
        self.action_salir.triggered.connect(self.salir)
        self.menu5.addAction(self.action_salir)
        self.menu5.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)

        self.menu2 = QMenu("Inventario", self)
        self.barra_menus1.addMenu(self.menu2)
        self.menu2.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)

        icon = QIcon()
        icon.addFile("productos_icon.png")
        self.action_crear_productos = QAction("Productos", self)
        self.action_crear_productos.setIcon(icon)  # Establece el icono para la acción
        self.action_crear_productos.triggered.connect(lambda: self.acceder_modulo("Productos"))
        self.menu2.addAction(self.action_crear_productos)

        icon = QIcon()
        icon.addFile("cargar_icon.png")
        self.action_cargos_de_productos = QAction("Cargos de Productos", self)
        self.action_cargos_de_productos.setIcon(icon)  # Establece el icono para la acción
        self.action_cargos_de_productos.triggered.connect(lambda: self.acceder_modulo("Cargos de Productos"))
        self.menu2.addAction(self.action_cargos_de_productos)

        icon = QIcon()
        icon.addFile("descargar_icon.png")
        self.action_descargos_de_productos = QAction("Descargos de Productos", self)
        self.action_descargos_de_productos.setIcon(icon)  # Establece el icono para la acción
        self.action_descargos_de_productos.triggered.connect(lambda: self.acceder_modulo("Descargos de Productos"))
        self.menu2.addAction(self.action_descargos_de_productos)

        self.menu2.addSeparator()  # Agrega un separador entre las acciones

        icon = QIcon()
        icon.addFile("ajuste_producto.png")
        self.action_ajuste_de_productos = QAction("Ajuste de Inventario", self)
        self.action_ajuste_de_productos.setIcon(icon)  # Establece el icono para la acción
        self.action_ajuste_de_productos.triggered.connect(lambda: self.acceder_modulo("Ajuste de Inventario"))
        self.menu2.addAction(self.action_ajuste_de_productos)

        icon = QIcon()
        icon.addFile("ajuste_precio.png")
        self.action_ajuste_de_precios = QAction("Ajuste de Precios", self)
        self.action_ajuste_de_precios.setIcon(icon)  # Establece el icono para la acción
        self.menu2.addAction(self.action_ajuste_de_precios)

        self.menu3 = QMenu("Transacciones", self)
        self.barra_menus1.addMenu(self.menu3)
        self.menu3.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)

        icon = QIcon()
        icon.addFile("monedas.png")
        self.action_monedas = QAction("Monedas", self)
        self.action_monedas.setIcon(icon)  # Establece el icono para la acción
        self.action_monedas.triggered.connect(lambda: self.acceder_modulo("Monedas"))
        self.menu3.addAction(self.action_monedas)

        icon = QIcon()
        icon.addFile("formas_pago.png")
        self.action_formas_de_pago = QAction("Formas de Pago", self)
        self.action_formas_de_pago.setIcon(icon)  # Establece el icono para la acción
        self.action_formas_de_pago.triggered.connect(lambda: self.acceder_modulo("Formas de Pago"))
        self.menu3.addAction(self.action_formas_de_pago)

        icon = QIcon()
        icon.addFile("impuestos.png")
        self.action_impuestos = QAction("Impuestos", self)
        self.action_impuestos.setIcon(icon)  # Establece el icono para la acción
        self.action_impuestos.triggered.connect(lambda: self.acceder_modulo("Impuestos"))
        self.menu3.addAction(self.action_impuestos)

        icon = QIcon()
        icon.addFile("tasa_c.png")
        self.action_tasa = QAction("Tasa Cambiaria", self)
        self.action_tasa.setIcon(icon)  # Establece el icono para la acción
        self.action_tasa.triggered.connect(lambda: self.acceder_modulo("Tasa Cambiaria"))
        self.menu3.addAction(self.action_tasa)

        self.menu3.addSeparator()  # Agrega un separador entre las acciones

        icon = QIcon()
        icon.addFile("compras.png")
        self.submenu = QMenu("Compras", self)
        self.submenu.setIcon(icon)  # Establece el icono para la acción
        self.menu3.addMenu(self.submenu)
        self.submenu.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)

        icon = QIcon()
        icon.addFile("proveedor.png")
        self.action_proveedores = QAction("Proveedores", self)
        self.action_proveedores.setIcon(icon)  # Establece el icono para la acción
        self.action_proveedores.triggered.connect(lambda: self.acceder_modulo("Proveedores"))
        self.submenu.addAction(self.action_proveedores)

        icon = QIcon()
        icon.addFile("orden_compra.png")
        self.action_ordenes_de_compra = QAction("Ordenes de Compra", self)
        self.action_ordenes_de_compra.setIcon(icon)
        self.action_ordenes_de_compra.triggered.connect(lambda: self.acceder_modulo("Ordenes de Compra"))
        self.submenu.addAction(self.action_ordenes_de_compra)

        icon = QIcon()
        icon.addFile("compra.png")
        self.action_compra_de_mercancia = QAction("Compra de Mercancia", self)
        self.action_compra_de_mercancia.setIcon(icon)
        self.action_compra_de_mercancia.triggered.connect(lambda: self.acceder_modulo("Compra de Mercancia"))
        self.submenu.addAction(self.action_compra_de_mercancia)
        
        icon = QIcon()
        icon.addFile("devolucion.png")
        self.action_devolucion_de_compra = QAction("Devolución de Compra", self)
        self.action_devolucion_de_compra.setIcon(icon)
        self.action_devolucion_de_compra.triggered.connect(lambda: self.acceder_modulo("Devolución de Compra"))
        self.submenu.addAction(self.action_devolucion_de_compra)

        self.action_cuentas_por_pagar = QAction("Cuentas por Pagar", self)
        self.submenu.addAction(self.action_cuentas_por_pagar)

        icon = QIcon()
        icon.addFile("ventas.png")
        self.submenu1 = QMenu("Ventas", self)
        self.submenu1.setIcon(icon)  # Establece el icono para la acción
        self.menu3.addMenu(self.submenu1)
        self.submenu1.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)

        self.action_proveedores1 = QAction("Cuentas por Cobrar", self)
        self.submenu1.addAction(self.action_proveedores1)

        self.action_ordenes_de_compra1 = QAction("Ordenes de Compra", self)
        self.submenu1.addAction(self.action_ordenes_de_compra1)

        self.action_Presupuestos = QAction("Presupuestos", self)
        self.submenu1.addAction(self.action_Presupuestos)

        self.menu4 = QMenu("Configuración", self)
        self.barra_menus1.addMenu(self.menu4)
        self.menu4.setStyleSheet("""
            QMenu {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item {
                background-color: #1bb0b0;
                color: #000000;
            }
            QMenu::item:selected {
                background-color: #1bb0b0; /* color de fondo deseado */
                color: #ffffff; /* color de texto deseado */
            }
        """)

        icon = QIcon()
        icon.addFile("c_general.png")
        self.action_general = QAction("General", self)
        self.action_general.triggered.connect(lambda: self.acceder_modulo("General"))
        self.action_general.setIcon(icon)
        self.menu4.addAction(self.action_general)

        icon = QIcon()
        icon.addFile("c_empresa.png")
        self.action_empresa = QAction("Empresa", self)
        self.action_empresa.setIcon(icon)
        self.action_empresa.triggered.connect(self.show_datos_empresa)
        self.menu4.addAction(self.action_empresa)

        self.menu4.addSeparator()  # Agrega un separador entre las acciones

        icon = QIcon()
        icon.addFile("c_acerca.png")
        self.action_acerca = QAction("Acerca de", self)
        self.action_acerca.setIcon(icon)
        self.action_acerca.triggered.connect(self.show_about_dialog)
        self.menu4.addAction(self.action_acerca)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("background-color: #47a2a2; border: 1px solid #ddd; padding: 5px; color: #ffffff;")

        # Obtiene el nombre del usuario que ha iniciado sesión
        self.usuario = login_window.username_input.text()
        # Obtiene el nivel del usuario
        self.cursor.execute("SELECT nivel FROM usuarios WHERE usuario = ?", (self.username,))
        result = self.cursor.fetchone()
        if result:
            self.nivel = result[0]
        else:
            self.nivel = "Desconocido"  # o cualquier otro valor por defecto

        self.usuario_label = QLabel(f"Usuario: {login_window.username_input.text()}            |            Nivel: {self.nivel}            |            Hora: {QDateTime.currentDateTime().toString('HH:mm:ss')}")
        self.usuario_label.setAlignment(Qt.AlignCenter)  # Ajusta la alineación del texto al centro
        self.status_bar.addPermanentWidget(self.usuario_label, 1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_hora)
        self.timer.start(1000)  # 1000 milisegundos = 1 segundo

        self.center_window(self)

        # Muestra la imagen de fondo al inicio
        self.show_image()

    def verificar_acceso(self, modulo):
        # Obtiene el código del usuario actual
        usuario_code = self.username  # O el método que uses para obtener el código del usuario

        # Cargar permisos del archivo JSON
        try:
            with open('permisos.json', 'r') as f:
                all_permisos = json.load(f)
                permisos_usuario = all_permisos.get(usuario_code, {})
                acceso = permisos_usuario.get("acceso", {})

                # Verifica si el módulo está permitido
                if acceso.get(modulo, False):
                    return True  # Acceso permitido
                else:
                    QMessageBox.warning(self, "Acceso Denegado", f"No tienes acceso a este módulo: {modulo}")
                    return False  # Acceso denegado
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No se encontraron permisos configurados.")
            return False  # Acceso denegado si no se encuentra el archivo

    def acceder_modulo(self, modulo):
        if self.verificar_acceso(modulo):
            if modulo == "Marcas de Inventario":
                if hasattr(self, 'crear_marcas_widget'):
                    self.stacked_widget.removeWidget(self.crear_marcas_widget)
                    self.crear_marcas_widget.deleteLater()
                self.crear_marcas_widget = ConfiguracionMarcas()
                self.stacked_widget.addWidget(self.crear_marcas_widget)
                self.stacked_widget.setCurrentWidget(self.crear_marcas_widget)
            elif modulo == "Lineas de Inventario":
                if hasattr(self, 'linea_widget'):
                    self.stacked_widget.removeWidget(self.linea_widget)
                    self.linea_widget.deleteLater()
                self.linea_widget = ConfiguracionLinea()
                self.stacked_widget.addWidget(self.linea_widget)
                self.stacked_widget.setCurrentWidget(self.linea_widget)
            elif modulo == "Depositos":
                if hasattr(self, 'configuracion_depositos_widget'):
                    self.stacked_widget.removeWidget(self.configuracion_depositos_widget)
                    self.configuracion_depositos_widget.deleteLater()
                self.configuracion_depositos_widget = ConfiguracionDepositos()
                self.stacked_widget.addWidget(self.configuracion_depositos_widget)
                self.stacked_widget.setCurrentWidget(self.configuracion_depositos_widget)
            elif modulo == "Productos":
                if hasattr(self, 'crear_productos_widget'):
                    self.stacked_widget.removeWidget(self.crear_productos_widget)
                    self.crear_productos_widget.deleteLater()
                self.crear_productos_widget = CrearProductos()
                self.stacked_widget.addWidget(self.crear_productos_widget)
                self.stacked_widget.setCurrentWidget(self.crear_productos_widget)
            elif modulo == "Cargos de Productos":
                if hasattr(self, 'cargar_productos_widget'):
                    self.stacked_widget.removeWidget(self.cargar_productos_widget)
                    self.cargar_productos_widget.deleteLater()
                self.cargar_productos_widget = CargarProductos()
                self.stacked_widget.addWidget(self.cargar_productos_widget)
                self.stacked_widget.setCurrentWidget(self.cargar_productos_widget)
            elif modulo == "Descargos de Productos":
                if hasattr(self, 'descargar_productos_widget'):
                    self.stacked_widget.removeWidget(self.descargar_productos_widget)
                    self.descargar_productos_widget.deleteLater()
                self.descargar_productos_widget = DescargarProductos()
                self.stacked_widget.addWidget(self.descargar_productos_widget)
                self.stacked_widget.setCurrentWidget(self.descargar_productos_widget)
            elif modulo == "Ajuste de Inventario":
                if hasattr(self, 'ajuste_productos_widget'):
                    self.stacked_widget.removeWidget(self.ajuste_productos_widget)
                    self.ajuste_productos_widget.deleteLater()
                self.ajuste_productos_widget = AjusteProductos()
                self.stacked_widget.addWidget(self.ajuste_productos_widget)
                self.stacked_widget.setCurrentWidget(self.ajuste_productos_widget)
            elif modulo == "Monedas":
                if hasattr(self, 'monedas_widget'):
                    self.stacked_widget.removeWidget(self.monedas_widget)
                    self.monedas_widget.deleteLater()
                self.monedas_widget = Monedas()
                self.stacked_widget.addWidget(self.monedas_widget)
                self.stacked_widget.setCurrentWidget(self.monedas_widget)
            elif modulo == "Formas de Pago":
                if hasattr(self, 'formas_pago_widget'):
                    self.stacked_widget.removeWidget(self.formas_pago_widget)
                    self.formas_pago_widget.deleteLater()
                self.formas_pago_widget = FormasDePago()
                self.stacked_widget.addWidget(self.formas_pago_widget)
                self.stacked_widget.setCurrentWidget(self.formas_pago_widget)
            elif modulo == "Impuestos":
                if hasattr(self, 'impuestos_widget'):
                    self.stacked_widget.removeWidget(self.impuestos_widget)
                    self.impuestos_widget.deleteLater()
                self.impuestos_widget = ConfiguracionImpuestos()
                self.stacked_widget.addWidget(self.impuestos_widget)
                self.stacked_widget.setCurrentWidget(self.impuestos_widget)
            elif modulo == "Tasa Cambiaria":
                if hasattr(self, 'tasa_c_widget'):
                    self.stacked_widget.removeWidget(self.tasa_c_widget)
                    self.tasa_c_widget.deleteLater()
                self.tasa_c_widget = MainWindow()
                self.stacked_widget.addWidget(self.tasa_c_widget)
                self.stacked_widget.setCurrentWidget(self.tasa_c_widget)
            elif modulo == "General":
                if hasattr(self, 'configuracion_general_widget'):
                    self.stacked_widget.removeWidget(self.configuracion_general_widget)
                    self.configuracion_general_widget.deleteLater()
                self.configuracion_general_widget = Configuracion()
                self.stacked_widget.addWidget(self.configuracion_general_widget)
                self.stacked_widget.setCurrentWidget(self.configuracion_general_widget)
            elif modulo == "Proveedores":
                if hasattr(self, 'proveedores_widget'):
                    self.stacked_widget.removeWidget(self.proveedores_widget)
                    self.proveedores_widget.deleteLater()
                self.proveedores_widget = Proveedores()
                self.stacked_widget.addWidget(self.proveedores_widget)
                self.stacked_widget.setCurrentWidget(self.proveedores_widget)

    def show_datos_empresa(self):
        datos_empresa = InformacionEmpresa()  # Crear una instancia del diálogo
        datos_empresa.exec_()

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)  # Crear una instancia del diálogo
        about_dialog.exec_()

    def mostrar_tasa_c(self):
        self.stacked_widget.setCurrentWidget(self.tasa_c_widget)

    def show_image(self):
        # Muestra el widget de imagen y luego cambia a la vista de funciones
        self.stacked_widget.setCurrentWidget(self.image_widget)

    def actualizar_hora(self):
        current_datetime = QDateTime.currentDateTime()
        self.usuario_label.setText(f"Usuario: {self.usuario}            |            Nivel: {self.nivel}            |            Fecha: {current_datetime.toString('dd-MM-yyyy')}            |            Hora: {current_datetime.toString('HH:mm:ss')}")

    def open_editor(self):
        self.editor = Editor()  # Crear una instancia del editor
        self.center_window(self.editor)
        self.editor.show()  # Mostrar la ventana del editor

    def run(self):
        self.show()

    def get_rol(self):
        self.cursor.execute("PRAGMA table_info('usuarios')")
        columns = self.cursor.fetchall()
        if not any(column[1] == 'rol' for column in columns):
            self.cursor.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT")
            self.cursor.execute("UPDATE usuarios SET rol = 'usuario'")
            self.conn.commit()

        # Agrega la columna sesion
        if not any(column[1] == 'sesion' for column in columns):
            self.cursor.execute("ALTER TABLE usuarios ADD COLUMN sesion TEXT")
            self.conn.commit()

    def salir(self):
        # Aquí se termina la sesión del usuario en la base de datos
        self.cursor.execute(f"UPDATE usuarios SET sesion = '0' WHERE usuario = '{self.usuario}'")
        self.conn.commit()
        self.conn.close()  # cierra la conexión a la base de datos
        self.close()
        self.login_window.username_input.clear()  # Vacía el campo de texto de usuario
        self.login_window.password_input.clear()  # Vacía el campo de texto de contraseña
        self.login_window.show()

    def center_window(self, window):
        screen_geometry = QApplication.desktop().availableGeometry()
        x = int((screen_geometry.width() - window.width()) / 2)
        y = int((screen_geometry.height() - window.height()) / 2)
        window.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    window = MainApplication(login_window)
    window.show()
    window.run()
    sys.exit(app.exec_())