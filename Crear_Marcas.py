import sys
from PyQt5.QtWidgets import QTabWidget, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QCheckBox, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QHeaderView, QApplication, QStatusBar, QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

conn = sqlite3.connect("Usuarios.db")  
cursor = conn.cursor()

class ConfiguracionMarcas(QDialog):
    def __init__(self):
        super().__init__()

        # Agrega una barra de estado a la ventana
        self.statusbar = QStatusBar()
        self.statusbar.setFixedHeight(25)

        self.setWindowTitle("Marcas de Inventario")
        self.setGeometry(100, 100, 700, 350)
        self.setWindowIcon(QIcon("icono.png"))  # Agrega el icono a la ventana

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.crear_tab_marcas(), "Marcas")
        self.tab_widget.tabBar().setStyleSheet("""
            QTabBar::tab {
            background-color: #008080; /* Color de fondo de las pestañas */
            border: 0.5px solid #ccc; /* Borde de las pestañas */
            padding: 5px; /* Espacio entre el texto y el borde */
            color: #ffffff;
            }
        """)

        self.disable_input_fields()

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.statusbar)  # Agrega la barra de estado al final del layout principal

        button_guardar = QPushButton("Guardar")
        button_guardar.clicked.connect(self.save_new_marca)
        button_guardar.setMaximumWidth(100)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)  # Alinear los botones hacia la derecha

        layout.addLayout(button_layout)  # Agrega el layout de botones al layout principal

        self.setLayout(layout)  # Agrega el layout principal a la ventana

    def crear_tab_marcas(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.imagen_cargos= QLabel(self)
        pixmap = QPixmap("z_marcas.png")
        self.imagen_cargos.setPixmap(pixmap)
        self.imagen_cargos.show()

        # Campos de entrada
        self.label_nombre = QLabel("Nombre:")
        self.edit_nombre = QLineEdit()
        self.edit_nombre.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
        self.edit_nombre.setFixedSize(235, 30)

        self.label_descripcion = QLabel("Descripción:")
        self.edit_descripcion = QTextEdit()

        # Botones
        self.button_add = QPushButton("Añadir Marca")
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
        self.button_add.clicked.connect(self.add_marca)

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
        self.button_modify.clicked.connect(self.modify_marca)
        self.button_modify.setEnabled(False)
        self.modify_mode = False  # Variable para indicar si el botón está en modo "Modificar" o "Guardar"

        # Tabla de monedas
        self.table_marcas = QTableWidget()
        self.table_marcas.setColumnCount(1)
        self.table_marcas.setHorizontalHeaderLabels(["Nombre"])
        self.table_marcas.horizontalHeader().setSectionResizeMode(0,  QHeaderView.Stretch)
        self.table_marcas.verticalHeader().setVisible(False)
        self.table_marcas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_marcas.setStyleSheet("QTableWidget::item:selected {\n"
        "                background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */\n"
        "                color: white; /* Color del texto de la fila seleccionada */\n"
        "            }\n"
        "            QHeaderView::section {\n"
        "                background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */\n"
        "                border: 5px;\n"
        "                color: #ffffff;\n"
        "            }")
        self.table_marcas.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_marcas.itemSelectionChanged.connect(self.cargar_marca_seleccionada)
        self.table_marcas.itemSelectionChanged.connect(self.selection_changed)
        self.table_marcas.keyPressEvent = self.delete_selected_marca

        # Layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.imagen_cargos)
        input_layout.addWidget(self.label_nombre)
        input_layout.addWidget(self.edit_nombre)
        input_layout.addWidget(self.label_descripcion)
        input_layout.addWidget(self.edit_descripcion)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_add)
        button_layout.addWidget(self.button_modify)
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

        self.button_cancel.clicked.connect(self.cancel_marca)
        button_layout.addWidget(self.button_cancel)
        button_layout.setAlignment(Qt.AlignRight)  # Alinear los botones hacia la derecha

        right_layout = QVBoxLayout()
        right_layout.addLayout(input_layout)
        right_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.table_marcas)
        main_layout.addLayout(right_layout)

        self.cargar_marcas()

        tab.setLayout(main_layout)

        return tab

    def delete_selected_marca(self, event):
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            selected_row = self.table_marcas.currentRow()
            if selected_row >= 0:
                marca_nombre = self.table_marcas.item(selected_row, 0).text()
                reply = QMessageBox.question(self, 'Eliminar marca', f'¿Estás seguro de eliminar la marca "{marca_nombre}"?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cursor.execute("DELETE FROM marcas WHERE nombre=?", (marca_nombre,))
                    conn.commit()
                    self.cargar_marcas()

    def disable_input_fields(self):
        self.edit_nombre.setEnabled(False)
        self.edit_descripcion.setEnabled(False)

    def enable_input_fields(self):
        self.edit_nombre.setEnabled(True)

    def cargar_marcas(self):
        # Carga las marcas desde la base de datos
        cursor.execute("SELECT * FROM marcas")
        marcas = cursor.fetchall()
        self.table_marcas.setRowCount(0)  # Limpiar la tabla
        for marca in marcas:
            row_position = self.table_marcas.rowCount()
            self.table_marcas.insertRow(row_position)
            self.table_marcas.setItem(row_position, 0, QTableWidgetItem(marca[1]))
        # Actualiza la barra de estado con la cantidad de marcas creadas
        self.statusbar.showMessage(f"Marcas creadas: {self.table_marcas.rowCount()}")

    def cargar_marca_seleccionada(self):
        # Obtener la fila seleccionada en la tabla
        selected_row = self.table_marcas.currentRow()
        if selected_row == -1:
            # No hay fila seleccionada, limpiar campos
            self.edit_nombre.setText("")
            self.edit_nombre.setEnabled(False)
            self.button_modify.setEnabled(False)  # Deshabilitar el botón si no hay selección
            return

        # Obtener los valores de la fila seleccionada
        nombre = self.table_marcas.item(selected_row, 0).text()

        # Cargar los valores en los campos de texto
        self.edit_nombre.setText(nombre)
        self.edit_nombre.setEnabled(False)
        self.button_modify.setEnabled(True)
        self.button_add.setEnabled(False)

    def selection_changed(self):
        if not self.table_marcas.selectionModel().hasSelection():
            self.edit_nombre.setText("")
            self.edit_nombre.setEnabled(False)
            self.button_modify.setEnabled(False)
            self.button_add.setEnabled(True)

    def add_marca(self):
        # Habilitar los campos de texto
        self.edit_nombre.setEnabled(True)
        self.enable_input_fields()

        # Cambiar el texto del botón a "Guardar"
        self.button_add.setText("Guardar")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.save_new_marca)

    def save_new_marca(self):
        # Obtener los valores de los campos de texto
        nombre = self.edit_nombre.text()

        # Insertar la nueva marca en la base de datos
        cursor.execute("INSERT INTO marcas (nombre) VALUES (?)", (nombre,))
        conn.commit()

        # Refrescar la tabla para mostrar la nueva marca
        self.table_marcas.setRowCount(0)  # Limpiar la tabla
        self.cargar_marcas()  # Cargar las marcas nuevamente

        # Deshabilitar los campos de texto y cambiar el texto del botón a "Añadir Impuesto"
        self.edit_nombre.setEnabled(False)
        self.button_add.setText("Añadir Marca")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_marca)

        # Limpia el campo de texto
        self.edit_nombre.clear()

    def modify_marca(self):
        if not self.modify_mode:
            self.edit_nombre.setEnabled(True)
            self.button_modify.setText("Guardar")
            self.button_modify.clicked.disconnect()
            self.button_modify.clicked.connect(self.save_marca_modificada)
            self.modify_mode = True

    def save_marca_modificada(self):
        # Obtener la fila seleccionada en la tabla
        selected_row = self.table_marcas.currentRow()
        if selected_row == -1:
            # No hay fila seleccionada, no guardar nada
            return

        # Obtener los valores de la fila seleccionada
        nombre = self.edit_nombre.text()
        id = selected_row + 1  # Assuming the id is the row number + 1

        # Actualizar la base de datos con los nuevos valores
        cursor.execute("UPDATE marcas SET nombre = ? WHERE id = ?", (nombre, id))
        conn.commit()

        # Refrescar la tabla para mostrar los cambios
        self.table_marcas.setRowCount(0)  # Limpiar la tabla
        self.cargar_marcas()  # Cargar los impuestos nuevamente

        # Volver a deshabilitar los campos y cambiar el botón a "Modificar"
        self.edit_nombre.setEnabled(False)
        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect()
        self.button_modify.clicked.connect(self.modify_marca)
        self.modify_mode = False

    def cancel_marca(self):
        # Limpiar el campo de texto
        self.edit_nombre.clear()

        # Deshabilitar los campos de texto
        self.edit_nombre.setEnabled(False)
        self.edit_descripcion.setEnabled(False)
        self.button_add.setEnabled(True)

        # Cambiar el texto del botón "Modificar" a "Modificar" y deshabilitarlo
        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect()
        self.button_modify.clicked.connect(self.modify_marca)
        self.button_modify.setEnabled(False)

        self.button_add.setText("Añadir Marca")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_marca)

        # Refrescar la tabla para mostrar los cambios
        self.table_marcas.setRowCount(0)  # Limpiar la tabla
        self.cargar_marcas()  # Cargar los impuestos nuevamente

        # Salir del modo de edición
        self.modify_mode = False

    def closeDB():
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = ConfiguracionMarcas()
    config.show()
    sys.exit(app.exec_())
    closeDB()  # Cierra la conexión a la base de datos