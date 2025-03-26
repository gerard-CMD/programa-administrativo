import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QLabel, QGraphicsScene, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
import sqlite3


class InformacionEmpresa(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = sqlite3.connect('Usuarios.db')  # Conectar a la base de datos
        self.cursor = self.conn.cursor()
        self.load_data()  # Cargar datos al iniciar

    def setupUi(self, MainWindow):
        self.setFixedSize(981, 561)
        self.setStyleSheet("background-color: rgb(243, 252, 250);")

        self.verticalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.datos_groupBox = QtWidgets.QGroupBox(MainWindow)
        self.datos_groupBox.setGeometry(QtCore.QRect(10, 110, 961, 401))
        self.datos_groupBox.setStyleSheet("QGroupBox {\n"
        "                color: #000000;\n"
        "                border: 1px solid #ccc; /* Borde del grupo */\n"
        "                border-radius: 5px; /* Radio del borde del grupo */\n"
        "                padding: 10px; /* Espacio entre el borde y el contenido */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.datos_groupBox.setObjectName("datos_groupBox")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.datos_groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 281, 155))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        self.vertical_Layout_datos_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.vertical_Layout_datos_1.setContentsMargins(0, 0, 0, 0)
        self.vertical_Layout_datos_1.setObjectName("vertical_Layout_datos_1")
        self.razon_social_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.razon_social_label.setObjectName("razon_social_label")
        self.vertical_Layout_datos_1.addWidget(self.razon_social_label)

        self.razon_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.razon_lineEdit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.razon_lineEdit.setObjectName("razon_lineEdit")
        self.vertical_Layout_datos_1.addWidget(self.razon_lineEdit)

        self.nombre_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.nombre_label.setObjectName("nombre_label")
        self.vertical_Layout_datos_1.addWidget(self.nombre_label)

        self.nombre_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.nombre_lineEdit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.nombre_lineEdit.setObjectName("nombre_lineEdit")
        self.vertical_Layout_datos_1.addWidget(self.nombre_lineEdit)

        self.rif_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.rif_label.setObjectName("rif_label")
        self.vertical_Layout_datos_1.addWidget(self.rif_label)

        self.rif_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.rif_lineEdit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.rif_lineEdit.setObjectName("rif_lineEdit")
        self.vertical_Layout_datos_1.addWidget(self.rif_lineEdit)

        self.line = QtWidgets.QFrame(self.datos_groupBox)
        self.line.setGeometry(QtCore.QRect(370, 20, 16, 371))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.imagen_cargos= QLabel(self)
        pixmap = QPixmap("info_empresa.png")
        self.imagen_cargos.setPixmap(pixmap)
        self.imagen_cargos.setGeometry(QtCore.QRect(90, 25, 790, 55))
        self.imagen_cargos.show()

        self.line_2 = QtWidgets.QFrame(self.datos_groupBox)
        self.line_2.setGeometry(QtCore.QRect(670, 20, 16, 371))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.datos_groupBox)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(390, 30, 281, 211))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")

        self.vertical_Layout_datos_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.vertical_Layout_datos_2.setContentsMargins(0, 0, 0, 0)
        self.vertical_Layout_datos_2.setObjectName("vertical_Layout_datos_2")
        
        self.telefono_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.telefono_label.setObjectName("telefono_label")
        self.vertical_Layout_datos_2.addWidget(self.telefono_label)

        self.telefono_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.telefono_lineEdit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.telefono_lineEdit.setObjectName("telefono_lineEdit")
        self.vertical_Layout_datos_2.addWidget(self.telefono_lineEdit)

        self.whatsapp_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.whatsapp_label.setObjectName("whatsapp_label")
        self.vertical_Layout_datos_2.addWidget(self.whatsapp_label)

        self.whatsapp_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.whatsapp_lineEdit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.whatsapp_lineEdit.setObjectName("whatsapp_lineEdit")
        self.vertical_Layout_datos_2.addWidget(self.whatsapp_lineEdit)

        self.correo_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.correo_label.setObjectName("correo_label")
        self.vertical_Layout_datos_2.addWidget(self.correo_label)

        self.correo_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.correo_lineEdit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.correo_lineEdit.setObjectName("correo_lineEdit")
        self.vertical_Layout_datos_2.addWidget(self.correo_lineEdit)

        self.pagina_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.pagina_label.setObjectName("pagina_label")
        self.vertical_Layout_datos_2.addWidget(self.pagina_label)

        self.pagina_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.pagina_lineEdit.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.pagina_lineEdit.setObjectName("pagina_lineEdit")
        self.vertical_Layout_datos_2.addWidget(self.pagina_lineEdit)

        self.logo_graphicsView = QtWidgets.QGraphicsView(self.datos_groupBox)
        self.logo_graphicsView.setGeometry(QtCore.QRect(690, 30, 261, 192))
        self.logo_graphicsView.setStyleSheet("QGraphicsView {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.logo_graphicsView.setObjectName("logo_graphicsView")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.datos_groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(720, 230, 211, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.boton_horizontal_Layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)

        self.boton_horizontal_Layout.setContentsMargins(0, 0, 0, 0)
        self.boton_horizontal_Layout.setSpacing(16)
        self.boton_horizontal_Layout.setObjectName("boton_horizontal_Layout")

        self.boton_agregar = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.boton_agregar.setStyleSheet("QPushButton {\n"
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
        self.boton_agregar.setObjectName("boton_agregar")
        self.boton_agregar.clicked.connect(self.load_logo)
        self.boton_horizontal_Layout.addWidget(self.boton_agregar)

        self.boton_eliminar = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.boton_eliminar.setStyleSheet("QPushButton {\n"
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
        self.boton_eliminar.setObjectName("boto_eliminar")
        self.boton_horizontal_Layout.addWidget(self.boton_eliminar)

        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.datos_groupBox)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 190, 361, 201))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.direccion_label = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.direccion_label.setObjectName("direccion_label")
        self.verticalLayout_6.addWidget(self.direccion_label)

        self.direccion_textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget_4)
        self.direccion_textEdit.setStyleSheet("QTextEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.direccion_textEdit.setObjectName("direccion_textEdit")
        self.verticalLayout_6.addWidget(self.direccion_textEdit)

        self.boton_aceptar = QtWidgets.QPushButton(MainWindow)
        self.boton_aceptar.setGeometry(QtCore.QRect(870, 520, 91, 31))
        self.boton_aceptar.setStyleSheet("QPushButton {\n"
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
        self.boton_aceptar.setObjectName("boton_aceptar")
        self.boton_aceptar.clicked.connect(self.save_data)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Informacion_empresa", "ZISCON ADMINISTRATIVO (V 1.0)"))
        MainWindow.setWindowIcon(QIcon('icono.png'))
        self.label.setText(_translate("Informacion_empresa", ""))
        self.datos_groupBox.setTitle(_translate("Informacion_empresa", "Datos de la empresa"))
        self.razon_social_label.setText(_translate("Informacion_empresa", "Razón Social"))
        self.nombre_label.setText(_translate("Informacion_empresa", "Nombre Comercial"))
        self.rif_label.setText(_translate("Informacion_empresa", "Rif ó ID Fiscal"))
        self.telefono_label.setText(_translate("Informacion_empresa", "Telefono de oficina"))
        self.whatsapp_label.setText(_translate("Informacion_empresa", "Whatsapp"))
        self.correo_label.setText(_translate("Informacion_empresa", "Correp Eléctronico"))
        self.pagina_label.setText(_translate("Informacion_empresa", "Pagina Web"))
        self.boton_agregar.setText(_translate("Informacion_empresa", "Agregar Logo"))
        self.boton_eliminar.setText(_translate("Informacion_empresa", "Eliminar"))
        self.direccion_label.setText(_translate("Informacion_empresa", "Dirección"))
        self.direccion_textEdit.setHtml(_translate("Informacion_empresa", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.boton_aceptar.setText(_translate("Informacion_empresa", "Aceptar"))

    def load_data(self):
        # Cargar datos de la base de datos
        self.cursor.execute("SELECT * FROM informacion_empresa LIMIT 1")  # Asumiendo que solo hay un registro
        row = self.cursor.fetchone()
        if row:
            self.razon_lineEdit.setText(str(row[1]))  # Ajusta el índice según la estructura de tu tabla
            self.nombre_lineEdit.setText(str(row[2]))
            self.rif_lineEdit.setText(str(row[3]))
            self.direccion_textEdit.setPlainText(str(row[4]))
            self.telefono_lineEdit.setText(str(row[5]))
            self.whatsapp_lineEdit.setText(str(row[6]))
            self.correo_lineEdit.setText(str(row[7]))
            self.pagina_lineEdit.setText(str(row[8]))
            self.load_logo_image(row[9])

        else:
            # Manejo de caso donde no hay datos
            self.razon_lineEdit.setText("")
            self.nombre_lineEdit.setText("")
            self.rif_lineEdit.setText("")
            self.direccion_textEdit.setPlainText("")
            self.telefono_lineEdit.setText("")
            self.whatsapp_lineEdit.setText("")
            self.correo_lineEdit.setText("")
            self.pagina_lineEdit.setText("")
            self.logo_graphicsView.setScene(QGraphicsScene())  # Limpiar el logo

    def load_logo_image(self, logo_path):
        if logo_path:
             pixmap = QPixmap(logo_path)

             # Obtener el tamaño del QGraphicsView
             view_width = self.logo_graphicsView.width()
             view_height = self.logo_graphicsView.height()

             # Escalar el pixmap al tamaño del QGraphicsView
             scaled_pixmap = pixmap.scaled(view_width, view_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

             # Crear una escena y agregar el pixmap escalado
             scene = QGraphicsScene()
             scene.addPixmap(scaled_pixmap)
             self.logo_graphicsView.setScene(scene)

    def load_logo(self):
        # Abrir un diálogo para seleccionar el logo
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Logo", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_name:
            self.save_logo_path(file_name)  # Guardar la ruta en la base de datos
            self.load_logo_image(file_name)  # Cargar el logo en el QGraphicsView

    def save_logo_path(self, logo_path):
        # Guardar la ruta del logo en la base de datos
        self.cursor.execute("UPDATE informacion_empresa SET logo_path = ? WHERE razon_social = ?", (logo_path, self.razon_lineEdit.text()))  # Ajusta la consulta según tu estructura
        self.conn.commit()  # Guardar cambios en la base de datos

    def save_data(self):
        # Guardar datos en la base de datos
        razon_social = self.razon_lineEdit.text()
        nombre_comercial = self.nombre_lineEdit.text()
        rif = self.rif_lineEdit.text()
        direccion = self.direccion_textEdit.toPlainText()
        telefono = self.telefono_lineEdit.text()
        whatsapp = self.whatsapp_lineEdit.text()
        correo = self.correo_lineEdit.text()
        pagina = self.pagina_lineEdit.text()

        # Aquí puedes usar un INSERT o UPDATE dependiendo de si ya existe un registro
        self.cursor.execute("""
            INSERT OR REPLACE INTO informacion_empresa (razon_social, nombre, rif, direccion, telefono_oficina, whatsapp, correo, sitio_web)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (razon_social, nombre_comercial, rif, direccion, telefono, whatsapp, correo, pagina))

        self.conn.commit()  # Guardar cambios en la base de datos

    def closeEvent(self, event):
        self.conn.close()  # Cerrar la conexión a la base de datos al cerrar la ventana
        event.accept()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = InformacionEmpresa()
    MainWindow.show()
    sys.exit(app.exec_())
