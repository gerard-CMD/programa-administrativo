import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QSpacerItem
)
from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import sqlite3
from utils import LoginWindow
from ventana_principal import MainApplication  # Importa la clase VentanaPrincipal
from AJUSTE_PRODUCTOS import AjusteProductos

class HoverLabel(QLabel):
    def __init__(self, icono_arriba_logo, icono_arriba_logo_hover):
        super().__init__()
        self.icono_arriba_logo = icono_arriba_logo
        self.icono_arriba_logo_hover = icono_arriba_logo_hover
        self.setPixmap(icono_arriba_logo.pixmap(QSize(16, 16)))

    def enterEvent(self, event):
        self.setPixmap(self.icono_arriba_logo_hover.pixmap(QSize(16, 16)))

    def leaveEvent(self, event):
        self.setPixmap(self.icono_arriba_logo.pixmap(QSize(16, 16)))

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.conn = sqlite3.connect("Usuarios.db")  # Conecta a la base de datos "Usuarios.db"
        self.cursor = self.conn.cursor()

        self.setWindowTitle("LOGIN - ZISCON ADMINISTRATIVO - Versión 1.0")
        self.setWindowIcon(QIcon("icono.png"))  # Agrega el icono a la ventana
        self.setFixedSize(580, 500)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Imagen en el lado izquierdo
        self.imagen_label = QLabel()
        self.imagen_label.setPixmap(QPixmap("background.jpg"))  # Reemplaza con la ruta de tu imagen

        # Ajusta el tamaño de la imagen para que se adapte al tamaño de la ventana
        self.imagen_label.setScaledContents(True)  # Permite que la imagen se escale
        self.imagen_label.setMargin(0)  # Elimina los márgenes de la imagen

        # Layout para la imagen
        imagen_layout = QVBoxLayout()
        imagen_layout.addWidget(self.imagen_label)

        # Ajusta el tamaño del layout para que se adapte al tamaño de la ventana
        imagen_layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes del layout
        imagen_layout.setSpacing(0)  # Elimina el espacio entre los elementos del layout
        imagen_layout.addStretch(1)  # Agrega un stretch para que el layout se estire

        icono_arriba_logo = QIcon("cerrarn.png")
        icono_arriba_logo_hover = QIcon("cerrar.png")  # Icono diferente para el estado de hover

        self.icono_arriba_logo_label = HoverLabel(icono_arriba_logo, icono_arriba_logo_hover)
        self.icono_arriba_logo_label.setStyleSheet("""
            QLabel {
                border: none; /* Elimina el borde del icono */
            }
            QLabel:hover {
                border: none; /* Elimina el borde del icono */
            }
        """)

        self.icono_arriba_logo_label.setParent(self)  # Establece la ventana principal como padre del icono
        self.icono_arriba_logo_label.move(555, 10)  # Posiciona el icono en la esquina superior DERECHA
        self.icono_arriba_logo_label.raise_()  # Eleva el icono al frente para que se muestre encima de otros widgets
        self.icono_arriba_logo_label.show()

        # Conecta el método clicked del icono a la función cerrar_ventana
        self.icono_arriba_logo_label.mousePressEvent = self.cerrar_ventana

        # Layout principal
        hbox = QHBoxLayout()
        hbox.addLayout(imagen_layout)  # Agrega la imagen al lado izquierdo
        hbox.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes del layout principal
        hbox.setSpacing(0)  # Elimina el espacio entre los elementos del layout principal

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("zisini.png")
        logo_label.setPixmap(pixmap)

        logo_layout = QHBoxLayout()
        logo_layout.addWidget(logo_label)
        logo_layout.addStretch(1)

        # Agrega un espacio negativo en la parte superior del layout
        logo_layout.setContentsMargins(0, 0, 0, 50)  # Ajusta el valor según sea necesario

        # Usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nombre de Usuario")
        self.username_input.setFixedWidth(200)
        self.username_input.setStyleSheet("background-color: #fff; border: 1px solid #ddd; padding: 5px;")

        # Agrega icono de usuario
        username_icon = QIcon("usuario.png")
        self.username_input.addAction(username_icon, QLineEdit.LeadingPosition)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)

        username_layout = QVBoxLayout()
        username_layout.addWidget(self.username_input)

        username_hbox = QHBoxLayout()
        username_hbox.addStretch(1)
        username_hbox.addLayout(username_layout)
        username_hbox.addStretch(1)

        # Contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(200)
        self.password_input.returnPressed.connect(self.login)
        self.password_input.setStyleSheet("background-color: #fff; border: 1px solid #ddd; padding: 5px;")

        # Agrega icono de contraseña
        password_icon = QIcon("contraseña.png")
        self.password_input.addAction(password_icon, QLineEdit.LeadingPosition)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; /* Color de fondo blanco */
                border: 1px solid #ccc; /* Borde gris claro */
                border-radius: 5px; /* Radio del borde */
                padding: 5px; /* Relleno */
                color: #000000; /* Color del texto negro */
            }
        """)

        self.username_input.returnPressed.connect(self.password_input.setFocus)

        password_layout = QVBoxLayout()
        password_layout.addWidget(self.password_input)

        password_hbox = QHBoxLayout()
        password_hbox.addStretch(1)
        password_hbox.addLayout(password_layout)
        password_hbox.addStretch(1)

        # Boton Login
        login_button = QPushButton("Iniciar Sesión")
        login_button.setFixedSize(128, 35)
        login_button.clicked.connect(self.login)

        # Establece la fuente del botón
        font = QFont("Poppins", 10, QFont.DemiBold)  # Fuente Poppins, tamaño 12, negrita
        login_button.setFont(font)

        login_button.setStyleSheet("""
            QPushButton {
                background-color: #47a2a2; 
                color: #fff; 
                border: none; 
                border-radius: 5px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #008080; /* Color cuando se coloca el cursor sobre el botón */
            }
        """)

        login_layout = QHBoxLayout()
        login_layout.addStretch(1)
        login_layout.addWidget(login_button)
        login_layout.addStretch(1)

        # Contenido existente en el lado derecho
        vbox = QVBoxLayout()
        vbox.addLayout(logo_layout)  # Agrega el layout del logo
        vbox.addLayout(username_hbox)  
        vbox.addSpacing(10)
        vbox.addLayout(password_hbox)
        vbox.addSpacing(20)
        vbox.addLayout(login_layout)

        # Centra el contenido en el lado derecho
        vbox.setAlignment(Qt.AlignCenter)

        # Centra el contenido en el lado derecho
        center_layout = QHBoxLayout()
        center_layout.addStretch(1)
        center_layout.addLayout(vbox)
        center_layout.addStretch(1)
        

        hbox.addLayout(center_layout)  # Agrega el contenido existente al lado derecho

        self.setLayout(hbox)

        # Agrega el estilo para el fondo de la ventana
        self.setStyleSheet("background-color: #ffffff;")

    #def keyPressEvent(self, event):
        #if event.key() == Qt.Key_Escape:
            #self.cerrar_ventana()
        #else:
            #super().keyPressEvent(event)

    def cerrar_ventana(self, _):
        self.close()

    def login(self):
        username = self.username_input.text().lower()  # Convertir a minúsculas
        password = self.password_input.text()

        if not username or not password:
            print("Campos vacíos")
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos")
            return
        
        self.cursor.execute("SELECT clave FROM usuarios WHERE usuario=?", (username,))
        row = self.cursor.fetchone()

        if row:
            stored_password = row[0]
            if password == stored_password:
                print("Inicio de sesión exitoso")
                self.close()  # Cierra la ventana de login
                self.ventana_principal = MainApplication(self)  # Crea una instancia de VentanaPrincipal
                self.ventana_principal.show()  # Muestra la ventana principal
            else:
                print("Credenciales incorrectas")
                QMessageBox.warning(self, "Error", "Credenciales incorrectas")
        else:
            print("Usuario no encontrado")
            QMessageBox.warning(self, "Error", "Usuario no encontrado")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())