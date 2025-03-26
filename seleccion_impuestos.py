from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

class SeleccionImpuestos(QtWidgets.QDialog):  # Hereda de QWidget
    def __init__(self):
        super().__init__()  # Llama al constructor de QWidget
        self.setupUi()

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
        self.iva_check.setGeometry(QtCore.QRect(7, 33, 81, 31))
        self.iva_check.setObjectName("iva_check")

        self.iva_percibido_check = QtWidgets.QCheckBox(self)
        self.iva_percibido_check.setGeometry(QtCore.QRect(7, 57, 101, 31))
        self.iva_percibido_check.setObjectName("iva_percibido_check")

        self.ial_check = QtWidgets.QCheckBox(self)
        self.ial_check.setGeometry(QtCore.QRect(7, 80, 101, 31))
        self.ial_check.setObjectName("ial_check")

        self.igtf_check = QtWidgets.QCheckBox(self)
        self.igtf_check.setGeometry(QtCore.QRect(7, 103, 101, 31))
        self.igtf_check.setObjectName("igtf_check")

        self.exento_check = QtWidgets.QCheckBox(self)
        self.exento_check.setGeometry(QtCore.QRect(7, 127, 101, 31))
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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = SeleccionImpuestos()  # Instancia de la clase
    window.show()
    sys.exit(app.exec_())
