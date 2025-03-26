import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QShortcut, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QTextEdit, QCheckBox, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QComboBox, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QDateTime
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

class Proveedores(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Proveedores")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icono.png"))

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.crear_tab_proveedor(), "Proveedores")
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
        
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addLayout(button_layout)  # Agregar el layout de botones al layout principal


        self.setLayout(layout)

        self.cargar_datos_proveedor()  # Cargar los datos de la base de datos

    def crear_tab_proveedor(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.imagen_cargos= QLabel(self)
        pixmap = QPixmap("z_proveedores.png")
        self.imagen_cargos.setPixmap(pixmap)
        self.imagen_cargos.show()

        # Campos de entrada
        self.label_codigo = QLabel("Código:")
        self.edit_codigo = QLineEdit()
        self.edit_codigo.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles

        self.label_nombre = QLabel("Razón Social:")
        self.edit_nombre = QLineEdit()
        self.edit_nombre.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles

        self.label_rif = QLabel("Rif:")
        self.edit_simbolo = QLineEdit()
        self.edit_simbolo.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles

        self.label_factor_pago = QLabel("Direccion:")
        self.edit_factor_pago = QTextEdit()
        self.edit_factor_pago.setMinimumHeight(20)  # Establecer la altura mínima en 30 píxeles

        self.label_persona_contacto = QLabel("Persona de Contacto:")
        self.edit_factor_inventario = QLineEdit()
        self.edit_factor_inventario.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles

        self.check_activo = QCheckBox("Activo")
        self.check_activo.setMaximumWidth(70)  # Establece el ancho máximo en 100 píxeles
        self.check_activo.setStyleSheet("""
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

        # Botones
        self.button_add = QPushButton("Crear")
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
        self.button_add.clicked.connect(self.add_moneda)

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
        self.button_modify.clicked.connect(self.modify_moneda)
        self.button_modify.setEnabled(False)

        self.button_delete = QPushButton("Eliminar")
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
        self.button_delete.clicked.connect(self.delete_moneda)
        self.button_delete.setEnabled(False)

        # Tabla de monedas
        self.table_monedas = QTableWidget()
        self.table_monedas.setColumnCount(2)
        self.table_monedas.setHorizontalHeaderLabels(["Código", "Nombre"])
        self.table_monedas.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_monedas.verticalHeader().setVisible(False)
        self.table_monedas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_monedas.setStyleSheet("QTableWidget::item:selected {\n"
        "                background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */\n"
        "                color: white; /* Color del texto de la fila seleccionada */\n"
        "            }\n"
        "            QHeaderView::section {\n"
        "                background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */\n"
        "                border: 5px;\n"
        "                color: #ffffff;\n"
        "            }")
        self.table_monedas.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_monedas.itemSelectionChanged.connect(self.load_selected_moneda)
        self.table_monedas.itemSelectionChanged.connect(self.selection_changed)

        # Layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.imagen_cargos)
        input_layout.addWidget(self.label_codigo)
        input_layout.addWidget(self.edit_codigo)
        input_layout.addWidget(self.label_nombre)
        input_layout.addWidget(self.edit_nombre)
        input_layout.addWidget(self.label_rif)
        input_layout.addWidget(self.edit_simbolo)
        input_layout.addWidget(self.label_factor_pago)
        input_layout.addWidget(self.edit_factor_pago)
        input_layout.addWidget(self.label_persona_contacto)
        input_layout.addWidget(self.edit_factor_inventario)
        input_layout.addWidget(self.check_activo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_add)
        button_layout.addWidget(self.button_modify)
        button_layout.addWidget(self.button_delete)
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
        self.button_cancel.clicked.connect(self.cancel_moneda)
        button_layout.addWidget(self.button_cancel)
        button_layout.setAlignment(Qt.AlignRight)  # Alinear los botones hacia la derecha

        right_layout = QVBoxLayout()
        right_layout.addLayout(input_layout)
        right_layout.addLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.table_monedas)
        main_layout.addLayout(right_layout)

        tab.setLayout(main_layout)

        return tab

    def disable_input_fields(self):
        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.edit_simbolo.setEnabled(False)
        self.edit_factor_pago.setEnabled(False)
        self.edit_factor_inventario.setEnabled(False)
        self.check_activo.setEnabled(False)
        self.check_activo.setChecked(False)

    def add_moneda(self):
        self.enable_input_fields()
        self.table_monedas.setEnabled(False)
        self.button_modify.setEnabled(False)
        self.button_delete.setEnabled(False)
        self.button_add.setText("Guardar cambios")
        self.button_add.clicked.disconnect(self.add_moneda)
        self.button_add.clicked.connect(self.save_new_moneda)

    def save_new_moneda(self):
        # Obtener los valores de los campos de entrada
        try:
            codigo = int(self.edit_codigo.text().strip())
            if codigo <= 0:
                raise ValueError("El código debe ser un entero positivo")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
            return
        nombre = self.edit_nombre.text()
        rif = self.edit_simbolo.text()
        direccion = self.edit_factor_pago.toPlainText()
        persona_contacto = self.edit_factor_inventario.text()
        activo = self.check_activo.isChecked()

        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Insertar la moneda en la base de datos
        cursor.execute("INSERT INTO proveedores (codigo, nombre, rif, direccion, persona_contacto, activo) VALUES (?, ?, ?, ?, ?, ?)",
                    (codigo, nombre, rif, direccion, persona_contacto, int(activo)))
        conn.commit()
        conn.close()

        # Agregar el proveedor a la tabla
        row = self.table_monedas.rowCount()
        self.table_monedas.insertRow(row)
        self.table_monedas.setItem(row, 0, QTableWidgetItem(str(codigo)))
        self.table_monedas.setItem(row, 1, QTableWidgetItem(nombre))
        self.table_monedas.setItem(row, 2, QTableWidgetItem(rif))
        self.table_monedas.setItem(row, 3, QTableWidgetItem(direccion))
        self.table_monedas.setItem(row, 4, QTableWidgetItem(persona_contacto))

        # Limpiar los campos de entrada
        self.clear_input_fields()

        # Mostrar un mensaje de confirmación
        QMessageBox.information(self, "Proveedor Creado", "El proveedor ha sido creado exitosamente")

        # Deshabilitar los campos de entrada
        self.table_monedas.setEnabled(True)
        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.edit_simbolo.setEnabled(False)
        self.edit_factor_pago.setEnabled(False)
        self.edit_factor_inventario.setEnabled(False)
        self.check_activo.setEnabled(False)
        self.button_add.setText("Añadir moneda")
        self.button_add.clicked.disconnect(self.save_new_moneda)

    def enable_input_fields(self):
        self.edit_codigo.setEnabled(True)
        self.edit_nombre.setEnabled(True)
        self.edit_simbolo.setEnabled(True)
        self.edit_factor_pago.setEnabled(True)
        self.edit_factor_inventario.setEnabled(True)
        self.check_activo.setEnabled(True)

    def cancel_moneda(self):
        self.table_monedas.setEnabled(True)
        self.clear_input_fields()
        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.edit_simbolo.setEnabled(False)
        self.edit_factor_pago.setEnabled(False)
        self.edit_factor_inventario.setEnabled(False)
        self.check_activo.setEnabled(False)
        self.button_modify.setText("Modificar")
        try:
            self.button_modify.clicked.disconnect(self.save_modified_moneda)
        except TypeError:
            pass
        self.button_modify.clicked.connect(self.modify_moneda)
        self.button_add.setText("Crear")
        try:
            self.button_add.clicked.disconnect(self.save_new_moneda)
        except TypeError:
            pass
        self.button_add.clicked.connect(self.add_moneda)

        self.table_monedas.setRowCount(0)
        self.load_moneda_data_into_table()

    def modify_moneda(self):
        self.table_monedas.setEnabled(False)
        row = self.table_monedas.currentRow()
        if row != -1:
            self.edit_codigo.setEnabled(False)
            self.edit_nombre.setEnabled(True)
            self.edit_simbolo.setEnabled(True)
            self.edit_factor_pago.setEnabled(True)
            self.edit_factor_inventario.setEnabled(True)
            self.check_activo.setEnabled(True)
            self.button_modify.setText("Guardar cambios")
            self.button_modify.clicked.disconnect(self.modify_moneda)
            self.button_modify.clicked.connect(self.save_modified_moneda)

    def save_modified_moneda(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        row = self.table_monedas.currentRow()
        if row != -1:
            try:
                try:
                    codigo = int(self.edit_codigo.text().strip())
                    if codigo <= 0:
                        raise ValueError("El código debe ser un entero positivo")
                except ValueError as e:
                    QMessageBox.warning(self, "Error", str(e))
                    return
                nombre = self.edit_nombre.text()
                rif = self.edit_simbolo.text()
                direccion = self.edit_factor_pago.toPlainText()
                persona_contacto = self.edit_factor_inventario.text().strip()
                activo = self.check_activo.isChecked()

                # Actualizar la moneda en la base de datos
                cursor.execute("UPDATE proveedores SET nombre = ?, rif = ?, direccion = ?, persona_contacto = ?, activo = ? WHERE codigo = ?",
                            (nombre, rif, direccion, persona_contacto, int(activo), codigo))
                conn.commit()

                # Actualizar la tabla de monedas
                self.table_monedas.setItem(row, 0, QTableWidgetItem(str(codigo)))
                self.table_monedas.setItem(row, 1, QTableWidgetItem(nombre))
                self.table_monedas.setItem(row, 2, QTableWidgetItem(rif))
                self.table_monedas.setItem(row, 3, QTableWidgetItem(direccion))
                self.table_monedas.setItem(row, 4, QTableWidgetItem(persona_contacto))

                # Mostrar un mensaje de confirmación
                QMessageBox.information(self, "Proveedor modificado", "El proveedor ha sido modificado correctamente")

                # Refrescar la tabla para mostrar los cambios
                self.table_monedas.setRowCount(0)  # Limpiar la tabla
                self.load_moneda_data_into_table()  # Cargar los impuestos nuevamente

                self.table_monedas.setEnabled(True)
                self.edit_codigo.setEnabled(False)
                self.edit_nombre.setEnabled(False)
                self.edit_simbolo.setEnabled(False)
                self.edit_factor_pago.setEnabled(False)
                self.edit_factor_inventario.setEnabled(False)
                self.check_activo.setEnabled(False)
                self.button_modify.setText("Modificar")
                self.button_modify.disconnect()
                self.button_modify.clicked.connect(self.modify_moneda)
            except ValueError:
                QMessageBox.warning(self, "Error", "Por favor, asegúrate de que todos los campos estén correctamente llenos.")

        conn.close()

    def delete_moneda(self):
        row = self.table_monedas.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ningún proveedor")
            return

        item = self.table_monedas.item(row, 1)  # Buscar el nombre del proveedor en la tabla
        if item is None:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ningún proveedor")
            return

        nombre = item.text()

        # Preguntar al usuario si está seguro de eliminar
        confirm = QMessageBox.question(self, "Confirmar eliminación", 
                                        f"¿Estás seguro de que deseas eliminar el proveedor '{nombre}'?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.No:
            return  # Si el usuario selecciona "No", salir de la función

        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Eliminar el proveedor de la base de datos
        cursor.execute("DELETE FROM proveedores WHERE nombre = ?", (nombre,))
        conn.commit()
        conn.close()

        # Eliminar la fila de la tabla
        self.table_monedas.removeRow(row)

        # Mostrar un mensaje de confirmación
        QMessageBox.information(self, "Proveedor eliminado", "El proveedor ha sido eliminado correctamente")

        # Vaciar los campos de entrada
        self.clear_input_fields()
        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.edit_simbolo.setEnabled(False)
        self.edit_factor_pago.setEnabled(False)
        self.edit_factor_inventario.setEnabled(False)
        self.check_activo.setEnabled(False)

    def clear_input_fields(self):
        self.edit_codigo.clear()
        self.edit_nombre.clear()
        self.edit_simbolo.clear()
        self.edit_factor_pago.clear()
        self.edit_factor_inventario.clear()
        self.check_activo.setChecked(False)

    def cargar_datos_proveedor(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        row = self.table_monedas.currentRow()
        if row != -1:
            item = self.table_monedas.item(row, 0)
            if item is not None:
                codigo = item.text()
                item = self.table_monedas.item(row, 1)
                if item is not None:
                    nombre = item.text()
                item = self.table_monedas.item(row, 2)
                if item is not None:
                    rif = item.text()
                item = self.table_monedas.item(row, 3)
                if item is not None:
                    direccion = item.text() 
                item = self.table_monedas.item(row, 4)
                if item is not None:
                    persona_contacto = item.text()   

                # Cargar los datos del proveedor en los campos de entrada
                self.edit_codigo.setText(codigo)
                self.edit_nombre.setText(nombre)
                self.edit_simbolo.setText(rif)
                self.edit_factor_pago.setText(direccion)
                self.edit_factor_inventario.setText(persona_contacto)
            else:
                self.clear_input_fields()
                self.edit_codigo.setEnabled(False)
                self.edit_nombre.setEnabled(False)
                self.edit_simbolo.setEnabled(False)
                self.edit_factor_pago.setEnabled(False)
                self.edit_factor_inventario.setEnabled(False)
                self.check_activo.setEnabled(False)

        # Consultar los proveedores en la base de datos
        cursor.execute("SELECT codigo, nombre, rif, direccion, persona_contacto, activo FROM proveedores")
        proveedores = cursor.fetchall()

        # Agregar los proveedores a la tabla
        self.table_monedas.setRowCount(0)  # Limpiar la tabla
        for row, proveedor in enumerate(proveedores):
            self.table_monedas.insertRow(row)
            self.table_monedas.setItem(row, 0, QTableWidgetItem(str(proveedor[0])))  # Mostrar el código
            self.table_monedas.setItem(row, 1, QTableWidgetItem(proveedor[1]))  # Mostrar el nombre

        conn.close()

    def load_moneda_data_into_table(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Consultar las monedas en la base de datos
        cursor.execute("SELECT codigo, nombre, rif, direccion, persona_contacto, activo FROM proveedores")
        monedas = cursor.fetchall()

        # Limpiar la tabla
        self.table_monedas.setRowCount(0)

        # Agregar las monedas a la tabla
        for row, moneda in enumerate(monedas):
            self.table_monedas.insertRow(row)
            self.table_monedas.setItem(row, 0, QTableWidgetItem(str(moneda[0])))  # Mostrar el código
            self.table_monedas.setItem(row, 1, QTableWidgetItem(moneda[1]))  # Mostrar el nombre
            self.table_monedas.setItem(row, 2, QTableWidgetItem(moneda[2]))  # Mostrar el rif

            # Agregar el checkbox a la tabla
            checkbox = QCheckBox()
            checkbox.setChecked(moneda[3] == 1)  # Establecer el estado del checkbox
            self.table_monedas.setCellWidget(row, 3, checkbox)  # Agregar el checkbox a la celda

        conn.close()

    def load_selected_moneda(self):
        row = self.table_monedas.currentRow()
        if row != -1:
            # Obtener el código del proveedor seleccionado
            codigo_item = self.table_monedas.item(row, 0)
            if codigo_item is not None:
                codigo = codigo_item.text()

                # Conectar a la base de datos
                conn = sqlite3.connect('Usuarios.db')
                cursor = conn.cursor()

                # Consultar todos los datos del proveedor usando el código
                cursor.execute("SELECT nombre, rif, direccion, persona_contacto, activo FROM proveedores WHERE codigo = ?", (codigo,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    nombre, rif, direccion, persona_contacto, activo = result

                    # Cargar los datos del proveedor en los campos de entrada
                    self.edit_codigo.setText(codigo)
                    self.edit_nombre.setText(nombre)
                    self.edit_simbolo.setText(rif)
                    self.edit_factor_pago.setText(direccion)
                    self.edit_factor_inventario.setText(persona_contacto)
                    self.check_activo.setChecked(bool(activo))  # Convertir a booleano
                    self.button_add.setEnabled(False)
                    self.button_modify.setEnabled(True)
                    self.button_delete.setEnabled(True)

    def selection_changed(self):
        if not self.table_monedas.selectionModel().hasSelection():
            self.edit_codigo.setText("")
            self.edit_nombre.setText("")
            self.edit_simbolo.setText("")
            self.edit_factor_pago.setText("")
            self.edit_factor_inventario.setText("")
            self.edit_codigo.setEnabled(False)
            self.edit_nombre.setEnabled(False)
            self.edit_simbolo.setEnabled(False)
            self.edit_factor_pago.setEnabled(False)
            self.edit_factor_inventario.setEnabled(False)
            self.check_activo.setEnabled(False)
            self.check_activo.setChecked(False)
            self.button_add.setEnabled(True)
            self.button_modify.setEnabled(False)
            self.button_delete.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = Proveedores()
    config.show()
    sys.exit(app.exec_())