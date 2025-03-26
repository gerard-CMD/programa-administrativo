import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sign Up")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QHBoxLayout()

        # Sección de la imagen
        self.image_label = QLabel(self)
        pixmap = QPixmap("ruta/a/tu/imagen.png")  # Reemplaza con la ruta a tu imagen
        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        # Sección de formularios
        form_layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.confirm_password_input)

        self.signup_button = QPushButton("Sign up")
        form_layout.addWidget(self.signup_button)

        self.account_label = QLabel("I have an account. Sign in.")
        form_layout.addWidget(self.account_label)

        layout.addLayout(form_layout)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignUpWindow()
    window.show()
    sys.exit(app.exec_())