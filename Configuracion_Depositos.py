import sys
from PyQt5.QtWidgets import QTabWidget, QMessageBox, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QCheckBox, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QHeaderView, QApplication, QShortcut
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

conn = sqlite3.connect("Usuarios.db")  
cursor = conn.cursor()

class ConfiguracionDepositos(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Configuración de Depositos")
        self.setGeometry(100, 100, 700, 350)
        self.setWindowIcon(QIcon("icono.png"))  # Agrega el icono a la ventana

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.crear_tab_depositos(), "Depositos")
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

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)  # Alinear los botones hacia la derecha

        layout.addLayout(button_layout)  # Agrega el layout de botones al layout principal

        self.setLayout(layout)  # Agrega el layout principal a la ventana

        self.button_add.setEnabled(False)
        self.button_modify.setEnabled(False)
        self.button_cancel.setEnabled(False)

        self.button_add.setDisabled(True)
        self.button_modify.setDisabled(True)
        self.button_cancel.setDisabled(True)

        # Estado de los botones
        self.buttons_enabled = False

        self.shortcut = QShortcut(Qt.CTRL + Qt.Key_D, self)
        self.shortcut.activated.connect(self.disabled_buttons)

        self.shortcut = QShortcut(Qt.CTRL + Qt.Key_H, self)
        self.shortcut.activated.connect(self.enable_buttons)

    def enable_buttons(self):
        self.buttons_enabled = True
        self.button_add.setEnabled(True)
        self.button_modify.setEnabled(False)
        self.button_cancel.setEnabled(True)

    def disabled_buttons(self):
        self.buttons_enabled = False
        self.button_add.setDisabled(True)
        self.button_modify.setDisabled(True)
        self.button_cancel.setDisabled(True)

    def crear_tab_depositos(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.imagen_cargos= QLabel(self)
        pixmap = QPixmap("z_depositos.png")
        self.imagen_cargos.setPixmap(pixmap)
        self.imagen_cargos.show()

        # Campos de entrada
        self.label_codigo = QLabel("Codigo:")
        self.edit_codigo = QLineEdit()
        self.edit_codigo.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
        self.edit_codigo.setFixedSize(235, 30)

        self.label_nombre = QLabel("Nombre:")
        self.edit_nombre = QLineEdit()
        self.edit_nombre.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
        self.edit_nombre.setFixedSize(235, 30)

        self.label_descripcion = QLabel("Descripción:")
        self.edit_descripcion = QTextEdit()

        # Botones
        self.button_add = QPushButton("Añadir Deposito")
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
        self.button_add.clicked.connect(self.add_Depositos)
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
        self.button_modify.clicked.connect(self.modify_deposito)
        self.modify_mode = False  # Variable para indicar si el botón está en modo "Modificar" o "Guardar"

        # Tabla de DEPOSITOS
        self.table_depositos = QTableWidget()
        self.table_depositos.setColumnCount(2)
        self.table_depositos.setHorizontalHeaderLabels(["Codigo", "Nombre"])
        self.table_depositos.horizontalHeader().setSectionResizeMode(1,  QHeaderView.Stretch)
        self.table_depositos.verticalHeader().setVisible(False)
        self.table_depositos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_depositos.setStyleSheet("QTableWidget::item:selected {\n"
        "                background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */\n"
        "                color: white; /* Color del texto de la fila seleccionada */\n"
        "            }\n"
        "            QHeaderView::section {\n"
        "                background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */\n"
        "                border: 5px;\n"
        "                color: #ffffff;\n"
        "            }")
        self.table_depositos.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_depositos.itemSelectionChanged.connect(self.load_depositos_selected)
        self.table_depositos.itemSelectionChanged.connect(self.selection_changed)
        self.table_depositos.keyPressEvent = self.delete_selected_deposito

        # Layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.imagen_cargos)
        input_layout.addWidget(self.label_codigo)
        input_layout.addWidget(self.edit_codigo)
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

        self.button_cancel.clicked.connect(self.cancel_deposito)
        button_layout.addWidget(self.button_cancel)
        button_layout.setAlignment(Qt.AlignRight)  # Alinear los botones hacia la derecha

        right_layout = QVBoxLayout()
        right_layout.addLayout(input_layout)
        right_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.table_depositos)
        main_layout.addLayout(right_layout)

        self.load_Depositos()

        tab.setLayout(main_layout)

        return tab

    def disable_input_fields(self):
        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.edit_descripcion.setEnabled(False)

    def enable_input_fields(self):
        self.edit_codigo.setEnabled(True)
        self.edit_nombre.setEnabled(True)

    def load_Depositos(self):
        try:
            # Carga los depositos desde la base de datos
            cursor.execute("SELECT codigo, nombre FROM depositos")
            depositos = cursor.fetchall()
            for deposito in depositos:
                row_position = self.table_depositos.rowCount()
                self.table_depositos.insertRow(row_position)
                self.table_depositos.setItem(row_position, 0, QTableWidgetItem(deposito[0]))
                self.table_depositos.setItem(row_position, 1, QTableWidgetItem(deposito[1]))
        except sqlite3.Error as e:
                print(f"Error al cargar depositos: {e}")

    def load_depositos_selected(self):
        # Obtener la fila seleccionada en la tabla
        selected_row = self.table_depositos.currentRow()
        if selected_row == -1:
            # No hay fila seleccionada, limpiar campos
            self.edit_codigo.setText("")
            self.edit_nombre.setText("")
            self.edit_codigo.setEnabled(False)
            self.edit_nombre.setEnabled(False)
            return

        # Obtener el código del depósito seleccionado
        codigo = self.table_depositos.item(selected_row, 0).text()

        # Conectar a la base de datos
        cursor.execute("SELECT * FROM depositos WHERE codigo = ?", (codigo,))
        deposito = cursor.fetchone()

        # Cargar los valores en los campos de texto
        self.edit_codigo.setText(deposito[1])
        self.edit_nombre.setText(deposito[2])

        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.button_modify.setEnabled(True)
        self.button_add.setEnabled(False)

    def selection_changed(self):
        if not self.table_depositos.selectionModel().hasSelection():
            self.edit_codigo.setText("")
            self.edit_nombre.setText("")
            self.edit_codigo.setEnabled(False)
            self.edit_nombre.setEnabled(False)
            self.button_modify.setEnabled(False)
            self.button_add.setEnabled(self.buttons_enabled)
        else:
            # Si hay una selección, habilita los botones solo si están permitidos
            self.button_modify.setEnabled(self.buttons_enabled)

    def add_Depositos(self):
        # Habilitar los campos de texto
        self.edit_codigo.setEnabled(True)
        self.edit_nombre.setEnabled(True)
        self.table_depositos.setEnabled(False)

        # Cambiar el texto del botón a "Guardar"
        self.button_add.setText("Guardar")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.save_new_deposito)

    def save_new_deposito(self):
        # Obtener los valores de los campos de texto
        codigo = self.edit_codigo.text()
        nombre = self.edit_nombre.text()

        # Insertar el nuevo depósito en la base de datos
        cursor.execute("INSERT INTO depositos (codigo, nombre) VALUES (?, ?)", (codigo, nombre))
        conn.commit()  # No olvides commit para guardar los cambios

        # Refrescar la tabla para mostrar el nuevo impuesto
        self.table_depositos.setRowCount(0)  # Limpiar la tabla
        self.load_Depositos()  # Cargar los impuestos nuevamente

        # Deshabilitar los campos de texto y cambiar el texto del botón a "Añadir Impuesto"
        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.table_depositos.setEnabled(True)
        self.button_add.setText("Añadir Impuesto")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_Depositos)

    def modify_deposito(self):
        if not self.modify_mode:
            self.table_depositos.setEnabled(False)
            self.edit_codigo.setEnabled(False)
            self.edit_nombre.setEnabled(True)
            self.button_modify.setText("Guardar")
            self.button_modify.clicked.disconnect()
            self.button_modify.clicked.connect(self.save_deposito_modification)
            self.modify_mode = True

    def save_deposito_modification(self):
        # Obtener la fila seleccionada en la tabla
        selected_row = self.table_depositos.currentRow()
        if selected_row == -1:
            # No hay fila seleccionada, no guardar nada
            return

        # Obtener los valores de la fila seleccionada
        codigo = self.edit_codigo.text()
        nombre = self.edit_nombre.text()

        # Actualizar el depósito en la base de datos
        cursor.execute("UPDATE depositos SET nombre = ? WHERE codigo = ?", (nombre, codigo))
        conn.commit()

        # Refrescar la tabla para mostrar los cambios
        self.table_depositos.setRowCount(0)  # Limpiar la tabla
        self.load_Depositos()  # Cargar los impuestos nuevamente

        # Volver a deshabilitar los campos y cambiar el botón a "Modificar"
        self.table_depositos.setEnabled(True)
        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect()
        self.button_modify.clicked.connect(self.modify_deposito)
        self.modify_mode = False

    def delete_selected_deposito(self, event):
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            selected_row = self.table_depositos.currentRow()
            if selected_row >= 1:
                deposito_nombre = self.table_depositos.item(selected_row, 1).text()
                reply = QMessageBox.question(self, 'Eliminar deposito', f'¿Estás seguro de eliminar el deposito "{deposito_nombre}"?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cursor.execute("DELETE FROM marcas WHERE nombre=?", (deposito_nombre,))
                    conn.commit()
                    self.load_Depositos()

    def cancel_deposito(self):
        # Limpiar el campo de texto
        self.edit_codigo.clear()
        self.edit_nombre.clear()

        # Deshabilitar los campos de texto
        self.table_depositos.setEnabled(True)
        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.edit_descripcion.setEnabled(False)
        self.button_add.setEnabled(True)

        # Cambiar el texto del botón "Modificar" a "Modificar" y deshabilitarlo
        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect()
        self.button_modify.clicked.connect(self.modify_deposito)
        self.button_modify.setEnabled(False)

        self.button_add.setText("Añadir Marca")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_Depositos)

        # Refrescar la tabla para mostrar los cambios
        self.table_depositos.setRowCount(0)  # Limpiar la tabla
        self.load_Depositos()  # Cargar los impuestos nuevamente

        # Salir del modo de edición
        self.modify_mode = False

    def closeDB():
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = ConfiguracionDepositos()
    config.show()
    sys.exit(app.exec_())
    closeDB()  # Cierra la conexión a la base de datos