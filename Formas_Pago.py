import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QCheckBox, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QComboBox, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

class FormasDePago(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect("Usuarios.db")
        self.cursor = self.conn.cursor()
        self.is_editing = False  # Agrega esta línea
        self.combo_moneda_asociada_list = []  # Crear una lista para almacenar los objetos QComboBox

        self.setWindowTitle("Formas de Pago")
        self.setGeometry(100, 100, 800, 450)
        self.setWindowIcon(QIcon("icono.png"))

        self.table_formas_pago = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.table_formas_pago)  # Agregar la tabla al layout

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.crear_tab_formas_pago(), "Formas de Pago")
        self.tab_widget.tabBar().setStyleSheet("""
            QTabBar::tab {
            background-color: #008080;  
            border: 0.5px solid #ccc;  
            padding: 5px;  
            color: #ffffff;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        
        self.setLayout(layout)  

    def crear_tab_formas_pago(self):
        tab = QWidget()
        main_layout = QHBoxLayout()

        self.imagen_cargos= QLabel(self)
        pixmap = QPixmap("z_formas_pago.png")
        self.imagen_cargos.setPixmap(pixmap)
        self.imagen_cargos.show()

        self.label_codigo = QLabel("Código:")
        self.edit_codigo = QLineEdit()
        self.edit_codigo.setMinimumHeight(30)
        self.label_descripcion = QLabel("Descripción:")
        self.edit_descripcion = QLineEdit()
        self.edit_descripcion.setMinimumHeight(30)

        self.label_origen_datos = QLabel("Origen de datos:")
        self.combo_origen_datos = QComboBox()
        self.combo_origen_datos.addItems(["Sin origen", "Bancos de la transacción", "Tarjetas de crédito"])

        self.label_tipo_forma = QLabel("Tipo de Forma:")
        self.combo_tipo_forma = QComboBox()
        self.combo_tipo_forma.addItems(["Forma de pago estandar", "Forma de Pago Extras"])

        self.label_moneda_asociada = QLabel("Moneda asociada:")
        self.combo_moneda_asociada = QComboBox()
        self.load_moneda_asociada_data(self.combo_moneda_asociada)

        self.label_activa = QLabel("Activo:")
        self.check_activa = QCheckBox()
        self.check_activa.setMaximumWidth(70)  # Establece el ancho máximo en 100 píxeles
        self.check_activa.setStyleSheet("""
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

        #Botones
        self.button_add = QPushButton("Agregar")
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
        self.button_add.clicked.connect(self.enable_fields)

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
        self.button_modify.clicked.connect(self.modify_forma_pago)

        self.button_delete = QPushButton("Eliminar")
        self.button_delete.clicked.connect(self.delete_forma_pago)
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
        self.button_cancel.clicked.connect(self.button_cancel_clicked)

        # Tabla de usuarios
        self.table_formas_pago.setColumnCount(2)
        self.table_formas_pago.setHorizontalHeaderLabels(["Código", "Descripción"])
        self.table_formas_pago.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_formas_pago.verticalHeader().setVisible(False)
        self.table_formas_pago.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_formas_pago.setStyleSheet("QTableWidget::item:selected {\n"
        "                background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */\n"
        "                color: white; /* Color del texto de la fila seleccionada */\n"
        "            }\n"
        "            QHeaderView::section {\n"
        "                background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */\n"
        "                border: 5px;\n"
        "                color: #ffffff;\n"
        "            }")
        self.table_formas_pago.itemSelectionChanged.connect(self.update_fields)
        self.table_formas_pago.itemSelectionChanged.connect(self.selection_changed)
        self.table_formas_pago.setColumnWidth(0, 50)  # Establecer ancho de la columna 0 (Código) a 50 píxeles
        
        # Campos de entrada
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.imagen_cargos)
        input_layout.addWidget(self.label_codigo)
        input_layout.addWidget(self.edit_codigo)
        input_layout.addWidget(self.label_descripcion)
        input_layout.addWidget(self.edit_descripcion)
        input_layout.addWidget(self.label_origen_datos)
        input_layout.addWidget(self.combo_origen_datos)
        input_layout.addWidget(self.label_tipo_forma)
        input_layout.addWidget(self.combo_tipo_forma)
        input_layout.addWidget(self.label_moneda_asociada)
        input_layout.addWidget(self.combo_moneda_asociada)
        input_layout.addWidget(self.label_activa)
        input_layout.addWidget(self.check_activa)  # Agregar el checkbox aquí

        # Botones
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_add)
        button_layout.addWidget(self.button_modify)
        button_layout.addWidget(self.button_delete)
        button_layout.addWidget(self.button_cancel)

        self.is_adding = True  # Variable para almacenar el estado actual del botón "Agregar"

        # Layout que contiene los campos de texto y botones
        right_layout = QVBoxLayout()
        right_layout.addLayout(input_layout)
        right_layout.addLayout(button_layout)

        # Agregar el widget table_formas_pago al layout main_layout
        main_layout.addWidget(self.table_formas_pago)
        main_layout.addLayout(right_layout)

        tab.setLayout(main_layout)

        self.edit_codigo.setEnabled(False)
        self.edit_descripcion.setEnabled(False)
        self.combo_origen_datos.setEnabled(False)
        self.combo_tipo_forma.setEnabled(False)
        self.combo_moneda_asociada.setEnabled(False)
        self.check_activa.setEnabled(False)

        tab.setLayout(main_layout)
        self.load_forma_pago_data()
        self.button_modify.setEnabled(False)
        self.button_delete.setEnabled(False)
        return tab

    def close_window(self):
        self.close()  # Cerrar la ventana

    def update_estatus(self):
        pass

    def update_fields(self):
        selected_row = self.table_formas_pago.currentRow()
        if selected_row is not None:
            item = self.table_formas_pago.item(selected_row, 0)
            if item is not None:
                codigo = item.text()
                self.cursor.execute("SELECT * FROM formas_pago WHERE codigo = ?", (codigo,))
                forma_pago = self.cursor.fetchone()
                if forma_pago:
                    self.edit_codigo.setText(forma_pago[0])
                    self.edit_descripcion.setText(forma_pago[1])
                    self.combo_origen_datos.setCurrentText(forma_pago[2])
                    self.combo_tipo_forma.setCurrentText(forma_pago[3])
                    
                    self.combo_moneda_asociada.setCurrentText(forma_pago[4])

                    self.check_activa.setChecked(forma_pago[5] == "Si")

    def enable_fields(self):
        self.is_adding = True
        self.table_formas_pago.setEnabled(False)
        self.edit_codigo.setEnabled(True)
        self.edit_descripcion.setEnabled(True)
        self.combo_origen_datos.setEnabled(True)
        self.combo_tipo_forma.setEnabled(True)
        self.combo_moneda_asociada.setEnabled(True)
        self.check_activa.setEnabled(True)
        self.button_add.setText("Guardar")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.save_forma_pago)

    def deshabilitar_campos(self):
        self.edit_codigo.setEnabled(False)
        self.edit_descripcion.setEnabled(False)
        self.combo_origen_datos.setEnabled(False)
        self.combo_moneda_asociada.setEnabled(False)
        self.combo_tipo_forma.setEnabled(False)
        self.check_activa.setEnabled(False)

    def load_moneda_asociada_data(self, combo_moneda_asociada):
        combo_moneda_asociada.clear()  # Limpiar el combobox
        self.cursor.execute("SELECT nombre FROM monedas")
        monedas = self.cursor.fetchall()
        for moneda in monedas:
            combo_moneda_asociada.addItem(moneda[0])  # Agregar cada moneda al combobox

    def save_forma_pago(self):
        codigo = self.edit_codigo.text()
        descripcion = self.edit_descripcion.text()
        origen_datos = self.combo_origen_datos.currentText()
        tipo_forma = self.combo_tipo_forma.currentText()
        moneda_asociada = self.combo_moneda_asociada.currentText()
        activa = "Si" if self.check_activa.isChecked() else "No"

        if self.is_adding:
            # Insertar nueva forma de pago
            self.cursor.execute("INSERT INTO formas_pago (codigo, descripcion, origen_datos, tipo_forma, moneda_asociada, activa) VALUES (?, ?, ?, ?, ?, ?)",
                                (codigo, descripcion, origen_datos, tipo_forma, moneda_asociada, activa))
        else:
            # Actualizar forma de pago existente
            self.cursor.execute("UPDATE formas_pago SET descripcion = ?, origen_datos = ?, tipo_forma = ?, moneda_asociada = ?, activa = ? WHERE codigo = ?",
                                (descripcion, origen_datos, tipo_forma, moneda_asociada, activa, codigo))

        self.conn.commit()  # Commit the changes to the database

        self.load_forma_pago_data()  # Actualizar la tabla con los nuevos datos
        self.edit_codigo.clear()
        self.edit_descripcion.clear()
        self.combo_origen_datos.setCurrentIndex(0)
        self.combo_tipo_forma.setCurrentIndex(0)
        self.combo_moneda_asociada.setCurrentIndex(0)
        self.deshabilitar_campos()
        self.table_formas_pago.setEnabled(True)
        self.check_activa.setChecked(False)
        self.button_add.setText("Agregar")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.enable_fields)
        self.is_adding = False

    def load_forma_pago_data(self):
        self.cursor.execute("SELECT codigo, descripcion FROM formas_pago")
        formas_pago = self.cursor.fetchall()
        self.table_formas_pago.setRowCount(len(formas_pago))
        for i, forma_pago in enumerate(formas_pago):
            self.table_formas_pago.setItem(i, 0, QTableWidgetItem(forma_pago[0]))
            self.table_formas_pago.setItem(i, 1, QTableWidgetItem(forma_pago[1]))

            combo_moneda_asociada = QComboBox()  # Crear un objeto QComboBox para cada fila
            self.load_moneda_asociada_data(combo_moneda_asociada)  # Cargar los datos en el objeto QComboBox
            self.table_formas_pago.setCellWidget(i, 2, combo_moneda_asociada)  # Asignar el objeto QComboBox a la celda
            self.combo_moneda_asociada_list.append(combo_moneda_asociada)  # Agregar el objeto QComboBox a la lista

    def clear_fields(self):
        self.edit_codigo.clear()
        self.edit_descripcion.clear()
        self.combo_origen_datos.setCurrentIndex(0)
        self.combo_tipo_forma.setCurrentIndex(0)
        self.combo_moneda_asociada.setCurrentIndex(0) # Restablece el índice del combo box
        self.check_activa.setChecked(False)

    def modify_forma_pago(self):
        self.table_formas_pago.setEnabled(False)
        selected_row = self.table_formas_pago.currentRow()
        if selected_row is not None:
            item = self.table_formas_pago.item(selected_row, 0)
            if item is not None:
                codigo = item.text()
                self.edit_codigo.setText(codigo)
                self.edit_codigo.setEnabled(False)
                self.edit_descripcion.setEnabled(True)
                self.combo_origen_datos.setEnabled(True)
                self.combo_tipo_forma.setEnabled(True)
                self.combo_moneda_asociada.setEnabled(True)
                self.check_activa.setEnabled(True)
                self.button_modify.setText("Guardar")
                self.button_modify.clicked.disconnect()
                self.button_modify.clicked.connect(self.save_modified_forma_pago)
            else:
                QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna fila para modificar")
        else:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna fila para modificar")

    def save_modified_forma_pago(self):
        codigo = self.edit_codigo.text()
        descripcion = self.edit_descripcion.text()
        origen_datos = self.combo_origen_datos.currentText()
        tipo_forma = self.combo_tipo_forma.currentText()
        moneda_asociada = self.combo_moneda_asociada.currentText()
        activa = "Si" if self.check_activa.isChecked() else "No"

        self.cursor.execute("UPDATE formas_pago SET descripcion = ?, origen_datos = ?, tipo_forma = ?, moneda_asociada = ?, activa = ? WHERE codigo = ?",
                            (descripcion, origen_datos, tipo_forma, moneda_asociada, activa, codigo))
        self.conn.commit()

        self.load_forma_pago_data()  # Actualizar la tabla con los nuevos datos
        self.edit_codigo.clear()
        self.edit_descripcion.clear()
        self.combo_origen_datos.setCurrentIndex(0)
        self.combo_tipo_forma.setCurrentIndex(0)
        self.combo_moneda_asociada.setCurrentIndex(0)
        self.check_activa.setChecked(False)
        self.deshabilitar_campos()
        self.table_formas_pago.setEnabled(True)
        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect()
        self.button_modify.clicked.connect(self.modify_forma_pago)

    def delete_forma_pago(self):
        selected_row = self.table_formas_pago.currentRow()
        if selected_row is not None:
            item = self.table_formas_pago.item(selected_row, 0)
            if item is not None:
                codigo = item.text()
                self.cursor.execute("DELETE FROM formas_pago WHERE codigo = ?", (codigo,))
                self.conn.commit()
                self.load_forma_pago_data()  # Actualizar la tabla con los nuevos datos
                self.clear_fields()
            else:
                QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna fila para eliminar")
        else:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna fila para eliminar")

    def button_cancel_clicked(self):
        self.clear_fields()
        self.table_formas_pago.setEnabled(True)
        self.edit_codigo.setEnabled(False)
        self.edit_descripcion.setEnabled(False)
        self.combo_origen_datos.setEnabled(False)
        self.combo_tipo_forma.setEnabled(False)
        self.combo_moneda_asociada.setEnabled(False)
        self.check_activa.setEnabled(False)
        self.button_add.setText("Agregar")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.enable_fields)
        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect()
        self.button_modify.clicked.connect(self.modify_forma_pago)

        self.table_formas_pago.setRowCount(0)
        self.load_forma_pago_data()

        self.is_adding = False

    def selection_changed(self):
        if not self.table_formas_pago.selectionModel().hasSelection():
            self.edit_codigo.setText("")
            self.edit_descripcion.setText("")
            self.edit_codigo.setEnabled(False)
            self.check_activa.setEnabled(False)
            self.check_activa.setChecked(False)
            self.button_add.setEnabled(True)
            self.button_modify.setEnabled(False)
            self.button_delete.setEnabled(False)
        else:
            # Si hay una selección, habilita los botones solo si están permitidos
            self.button_modify.setEnabled(True)
            self.button_add.setEnabled(False)
            self.button_delete.setEnabled(True)

    def closeEvent(self, event):
        self.conn.commit()
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = FormasDePago()
    config.show()
    sys.exit(app.exec_())