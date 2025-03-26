# utils.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        # Agrega tus widgets de login aquí

    def show(self):
        super().show()

class MainApplication(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window

        self.setWindowTitle("JG TECHNOLOGY ADMINISTRATIVO")
        self.setGeometry(100, 100, 800, 600)

        self.barra_menus1 = QMenuBar(self)
        self.setMenuBar(self.barra_menus1)

        self.menu = QMenu("Archivo", self)
        self.barra_menus1.addMenu(self.menu)

        self.action_salir = QAction("Salir", self)
        self.action_salir.triggered.connect(self.salir)
        self.menu.addAction(self.action_salir)

        self.menu2 = QMenu("Inventario", self)
        self.barra_menus1.addMenu(self.menu2)

        self.action_productos = QAction("Productos", self)
        self.menu2.addAction(self.action_productos)

        self.action_crear_productos = QAction("Crear Productos", self)
        self.menu2.addAction(self.action_crear_productos)

        self.action_cargos_de_productos = QAction("Cargos de Productos", self)
        self.menu2.addAction(self.action_cargos_de_productos)

        self.action_descargos_de_productos = QAction("Descargos de Productos", self)
        self.menu2.addAction(self.action_descargos_de_productos)

        self.action_transferencia_de_productos = QAction("Transferencia de Productos", self)
        self.menu2.addAction(self.action_transferencia_de_productos)

        self.action_ajuste_de_productos = QAction("Ajuste de Productos", self)
        self.menu2.addAction(self.action_ajuste_de_productos)

        self.action_ajuste_de_precios = QAction("Ajuste de Precios", self)
        self.menu2.addAction(self.action_ajuste_de_precios)

        self.menu3 = QMenu("Transacciones", self)
        self.barra_menus1.addMenu(self.menu3)

        self.action_monedas = QAction("Monedas", self)
        self.menu3.addAction(self.action_monedas)

        self.action_formas_de_pago = QAction("Formas de Pago", self)
        self.menu3.addAction(self.action_formas_de_pago)

        self.submenu = QMenu("Compras", self)
        self.menu3.addMenu(self.submenu)

        self.action_proveedores = QAction("Proveedores", self)
        self.submenu.addAction(self.action_proveedores)

        self.action_ordenes_de_compra = QAction("Ordenes de Compra", self)
        self.submenu.addAction(self.action_ordenes_de_compra)

        self.action_compra_de_mercancia = QAction("Compra de Mercancia", self)
        self.submenu.addAction(self.action_compra_de_mercancia)

        self.action_devolucion_de_compra = QAction("Devolución de Compra", self)
        self.submenu.addAction(self.action_devolucion_de_compra)

        self.action_cuentas_por_pagar = QAction("Cuentas por Pagar", self)
        self.submenu.addAction(self.action_cuentas_por_pagar)

        self.submenu1 = QMenu("Ventas", self)
        self.menu3.addMenu(self.submenu1)

        self.action_proveedores1 = QAction("Proveedores", self)
        self.submenu1.addAction(self.action_proveedores1)

        self.action_ordenes_de_compra1 = QAction("Ordenes de Compra", self)
        self.submenu1.addAction(self.action_ordenes_de_compra1)

    def run(self):
        self.show()

    def salir(self):
        self.close()
        self.login_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    window = MainApplication(login_window)
    window.run()
    sys.exit(app.exec_())