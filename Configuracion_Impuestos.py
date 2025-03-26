import sys
from PyQt5.QtWidgets import QTabWidget, QMessageBox, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QCheckBox, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QAbstractItemView, QHeaderView, QApplication, QShortcut
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

conn = sqlite3.connect("Usuarios.db")  
cursor = conn.cursor()

class ConfiguracionImpuestos(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Configuración de Impuestos")
        self.setGeometry(100, 100, 700, 350)
        self.setWindowIcon(QIcon("icono.png"))  # Agrega el icono a la ventana

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.crear_tab_impuestos(), "Impuestos")
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

        button_guardar = QPushButton("Guardar")
        button_guardar.clicked.connect(self.save_new_impuesto)
        button_guardar.setMaximumWidth(100)

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

    def crear_tab_impuestos(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.imagen_cargos= QLabel(self)
        pixmap = QPixmap("z_impuestos.png")
        self.imagen_cargos.setPixmap(pixmap)
        self.imagen_cargos.show()

        # Campos de entrada
        self.label_nombre = QLabel("Nombre:")
        self.edit_nombre = QLineEdit()
        self.edit_nombre.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
        self.edit_nombre.setFixedSize(235, 30)
        self.label_porcentaje = QLabel("Porcentaje:")
        self.edit_porcentaje = QLineEdit()
        self.edit_porcentaje.setFixedSize(235, 30)
        self.label_descripcion = QLabel("Descripción:")
        self.edit_descripcion = QTextEdit()
        self.checkbox_activo = QCheckBox("Activo")
        self.checkbox_activo.setStyleSheet("""
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
        self.checkbox_activo.setChecked(True)  # Por defecto, el impuesto está activo

        # Crear QComboBox para seleccionar la base
        self.combo_base = QComboBox()
        self.combo_base.addItem("")
        self.combo_base.addItem("Base Imponible")
        self.combo_base.addItem("Base Percibido")
        self.combo_base.addItem("Base Monto Moneda")

        # Botones
        self.button_add = QPushButton("Añadir Impuesto")
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
        self.button_add.clicked.connect(self.add_Impuesto)
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
        self.button_modify.clicked.connect(self.modify_impuesto)
        self.modify_mode = False  # Variable para indicar si el botón está en modo "Modificar" o "Guardar"

        # Tabla de monedas
        self.table_impuestos = QTableWidget()
        self.table_impuestos.setColumnCount(2)
        self.table_impuestos.setHorizontalHeaderLabels(["Nombre", "Porcentaje"])
        self.table_impuestos.horizontalHeader().setSectionResizeMode(0,  QHeaderView.Stretch)
        self.table_impuestos.verticalHeader().setVisible(False)
        self.table_impuestos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_impuestos.setStyleSheet("QTableWidget::item:selected {\n"
        "                background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */\n"
        "                color: white; /* Color del texto de la fila seleccionada */\n"
        "            }\n"
        "            QHeaderView::section {\n"
        "                background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */\n"
        "                border: 5px;\n"
        "                color: #ffffff;\n"
        "            }")
        self.table_impuestos.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_impuestos.itemSelectionChanged.connect(self.load_impuesto_selected)
        self.table_impuestos.itemSelectionChanged.connect(self.selection_changed)
        self.table_impuestos.keyPressEvent = self.delete_selected_impuesto

        # Layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.imagen_cargos)
        input_layout.addWidget(self.label_nombre)
        input_layout.addWidget(self.edit_nombre)
        input_layout.addWidget(self.label_porcentaje)
        input_layout.addWidget(self.edit_porcentaje)
        input_layout.addWidget(self.label_descripcion)
        input_layout.addWidget(self.edit_descripcion)
        input_layout.addWidget(QLabel("Base para el cálculo:"))  # Etiqueta para el combo box
        input_layout.addWidget(self.combo_base)
        input_layout.addWidget(self.checkbox_activo)

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

        self.button_cancel.clicked.connect(self.cancel_impuesto)
        button_layout.addWidget(self.button_cancel)
        button_layout.setAlignment(Qt.AlignRight)  # Alinear los botones hacia la derecha

        right_layout = QVBoxLayout()
        right_layout.addLayout(input_layout)
        right_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.table_impuestos)
        main_layout.addLayout(right_layout)

        self.load_Impuestos()

        tab.setLayout(main_layout)

        return tab
    
    def disable_input_fields(self):
        self.edit_nombre.setEnabled(False)
        self.edit_porcentaje.setEnabled(False)
        self.edit_descripcion.setEnabled(False)
        self.checkbox_activo.setEnabled(False)
        self.checkbox_activo.setChecked(False)
        self.combo_base.setEnabled(False)

    def enable_input_fields(self):
        self.edit_nombre.setEnabled(True)
        self.edit_porcentaje.setEnabled(True)

    def load_Impuestos(self):
        # Carga los impuestos desde la base de datos
        cursor.execute("SELECT * FROM impuestos")
        impuestos = cursor.fetchall()
        for impuesto in impuestos:
            row_position = self.table_impuestos.rowCount()
            self.table_impuestos.insertRow(row_position)
            self.table_impuestos.setItem(row_position, 0, QTableWidgetItem(impuesto[1]))
            self.table_impuestos.setItem(row_position, 1, QTableWidgetItem(str(impuesto[2])))

    def update_impuesto_estado(self, activo):
        # Obtener la fila seleccionada en la tabla
        selected_row = self.table_impuestos.currentRow()
        if selected_row == -1:
            return  # No hay fila seleccionada

        # Obtener el nombre del impuesto seleccionado
        nombre = self.table_impuestos.item(selected_row, 0).text()

        # Obtener el estado del CheckBox
        activo = 1 if self.checkbox_activo.isChecked() else 0

        # Actualizar el estado en la base de datos
        cursor.execute("UPDATE impuestos SET activo = ? WHERE nombre = ?", (activo, nombre))
        conn.commit()

    def load_impuesto_selected(self):
        # Obtener la fila seleccionada en la tabla
        selected_row = self.table_impuestos.currentRow()
        if selected_row == -1:
            # No hay fila seleccionada, limpiar campos
            self.edit_nombre.setText("")
            self.edit_porcentaje.setText("")
            self.edit_nombre.setEnabled(False)
            self.edit_porcentaje.setEnabled(False)
            self.checkbox_activo.setChecked(False)
            self.combo_base.setEnabled(False)
            self.combo_base.setCurrentIndex(0)  # Restablecer el combobox a la opción vacía
            return

        # Obtener los valores de la fila seleccionada
        nombre = self.table_impuestos.item(selected_row, 0).text()
        porcentaje = self.table_impuestos.item(selected_row, 1).text()

        # Obtener el estado activo del impuesto desde la base de datos
        cursor.execute("SELECT activo, metodo_calculo FROM impuestos WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        activo = resultado[0]
        metodo_calculo = resultado[1]

        # Cargar los valores en los campos de texto
        self.edit_nombre.setText(nombre)
        self.edit_porcentaje.setText(porcentaje)
        self.checkbox_activo.setChecked(activo == 1)
        self.combo_base.setCurrentText(metodo_calculo)  # Establecer el método de cálculo en el combobox

        self.update_impuesto_estado(activo)

        self.edit_nombre.setEnabled(False)
        self.edit_porcentaje.setEnabled(False)
        self.checkbox_activo.setEnabled(False)

    def selection_changed(self):
        if not self.table_impuestos.selectionModel().hasSelection():
            self.edit_nombre.setText("")
            self.edit_porcentaje.setText("")
            self.edit_nombre.setEnabled(False)
            self.edit_porcentaje.setEnabled(False)
            self.checkbox_activo.setEnabled(False)
            self.checkbox_activo.setChecked(False)
            self.combo_base.setCurrentIndex(0)
            self.button_modify.setEnabled(False)
            self.button_add.setEnabled(self.buttons_enabled)
        else:
            # Si hay una selección, habilita los botones solo si están permitidos
            self.button_modify.setEnabled(self.buttons_enabled)
            self.button_add.setEnabled(False)

    def add_Impuesto(self):
        # Habilitar los campos de texto
        self.edit_nombre.setEnabled(True)
        self.edit_porcentaje.setEnabled(True)
        self.checkbox_activo.setEnabled(True)
        self.combo_base.setEnabled(True)
        self.table_impuestos.setEnabled(False)

        # Cambiar el texto del botón a "Guardar"
        self.button_add.setText("Guardar")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.save_new_impuesto)

    def save_new_impuesto(self):
        # Obtener los valores de los campos de texto
        nombre = self.edit_nombre.text()
        porcentaje = self.edit_porcentaje.text()
        activo = 1 if self.checkbox_activo.isChecked() else 0

        # Obtener el valor seleccionado del QComboBox
        metodo_calculo = self.combo_base.currentText()  # Obtener el texto de la opción seleccionada

        # Insertar el nuevo impuesto en la base de datos
        cursor.execute("INSERT INTO impuestos (nombre, porcentaje, activo, metodo_calculo) VALUES (?, ?, ?, ?)",
                    (nombre, float(porcentaje.replace("%", "")) / 100, activo, metodo_calculo))
        conn.commit()

        # Refrescar la tabla para mostrar el nuevo impuesto
        self.table_impuestos.setRowCount(0)  # Limpiar la tabla
        self.load_Impuestos()  # Cargar los impuestos nuevamente

        # Deshabilitar los campos de texto y cambiar el texto del botón a "Añadir Impuesto"
        self.table_impuestos.setEnabled(True)
        self.edit_nombre.setEnabled(False)
        self.edit_porcentaje.setEnabled(False)
        self.checkbox_activo.setEnabled(False)
        self.combo_base.setCurrentIndex(0)
        self.button_add.setText("Añadir Impuesto")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_Impuesto)

    def modify_impuesto(self):
        if not self.modify_mode:
            self.table_impuestos.setEnabled(False)
            self.edit_nombre.setEnabled(True)
            self.edit_porcentaje.setEnabled(True)
            self.checkbox_activo.setEnabled(True)
            self.combo_base.setEnabled(True)
            self.button_modify.setText("Guardar")
            self.button_modify.clicked.disconnect()
            self.button_modify.clicked.connect(self.save_impuesto_modification)
            self.modify_mode = True

    def save_impuesto_modification(self):
        # Obtener la fila seleccionada en la tabla
        selected_row = self.table_impuestos.currentRow()
        if selected_row == -1:
            # No hay fila seleccionada, no guardar nada
            return

        # Obtener los valores de la fila seleccionada
        nombre = self.edit_nombre.text()
        porcentaje = self.edit_porcentaje.text()
        activo = 1 if self.checkbox_activo.isChecked() else 0

        # Obtener el valor seleccionado del QComboBox
        metodo_calculo = self.combo_base.currentText()  # Obtener el texto de la opción seleccionada

        # Actualizar la base de datos con los nuevos valores
        cursor.execute("UPDATE impuestos SET nombre = ?, porcentaje = ?, activo = ?, metodo_calculo = ? WHERE id = ?",
                       (nombre, float(porcentaje.replace("%", "")) / 100, activo, metodo_calculo, selected_row + 1))
        conn.commit()

        # Refrescar la tabla para mostrar los cambios
        self.table_impuestos.setRowCount(0)  # Limpiar la tabla
        self.load_Impuestos()  # Cargar los impuestos nuevamente

        # Volver a deshabilitar los campos y cambiar el botón a "Modificar"
        self.table_impuestos.setEnabled(True)
        self.edit_nombre.setEnabled(False)
        self.edit_porcentaje.setEnabled(False)
        self.checkbox_activo.setEnabled(False)
        self.combo_base.setCurrentIndex(0)
        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect()
        self.button_modify.clicked.connect(self.modify_impuesto)
        self.modify_mode = False

    def delete_selected_impuesto(self, event):
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            selected_row = self.table_impuestos.currentRow()
            if selected_row >= 0:
                impuesto_nombre = self.table_impuestos.item(selected_row, 0).text()
                reply = QMessageBox.question(self, 'Eliminar impuesto', f'¿Estás seguro de eliminar el impuesto: "{impuesto_nombre}"?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cursor.execute("DELETE FROM impuestos WHERE nombre=?", (impuesto_nombre,))
                    conn.commit()
                    # Eliminar la fila de la tabla
                    self.table_impuestos.removeRow(selected_row)

    def cancel_impuesto(self):
        # Limpiar el campo de texto
        self.edit_nombre.clear()
        self.edit_porcentaje.clear()
        self.checkbox_activo.setCheckable(True)
        self.combo_base.setCurrentIndex(0)

        # Deshabilitar los campos de texto
        self.table_impuestos.setEnabled(True)
        self.edit_nombre.setEnabled(False)
        self.edit_porcentaje.setEnabled(False)
        self.edit_descripcion.setEnabled(False)
        self.checkbox_activo.setEnabled(False)
        self.combo_base.setEnabled(False)
        self.button_add.setEnabled(True)

        # Cambiar el texto del botón "Modificar" a "Modificar" y deshabilitarlo
        self.button_modify.setText("Modificar")
        self.button_modify.clicked.disconnect()
        self.button_modify.clicked.connect(self.modify_impuesto)
        self.button_modify.setEnabled(False)

        self.button_add.setText("Añadir Impuesto")
        self.button_add.clicked.disconnect()
        self.button_add.clicked.connect(self.add_Impuesto)

        # Refrescar la tabla para mostrar los cambios
        self.table_impuestos.setRowCount(0)  # Limpiar la tabla
        self.load_Impuestos()  # Cargar los impuestos nuevamente

        # Salir del modo de edición
        self.modify_mode = False

    def closeDB():
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = ConfiguracionImpuestos()
    config.show()
    sys.exit(app.exec_())
    closeDB()  # Cierra la conexión a la base de datos