import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QShortcut, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QCheckBox, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QComboBox, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QDateTime
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

class Monedas(QWidget):
    def __init__(self):
        super().__init__()
        self.create_columns()  # Llamar al método create_columns
        self.is_new_moneda = False  # Variable de instancia para indicar si se está creando una nueva moneda

        self.setWindowTitle("Monedas")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icono.png"))

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.crear_tab_monedas(), "Monedas")
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

        self.load_moneda_data()  # Cargar los datos de la base de datos

    def crear_tab_monedas(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.imagen_cargos= QLabel(self)
        pixmap = QPixmap("z_monedas.png")
        self.imagen_cargos.setPixmap(pixmap)
        self.imagen_cargos.show()

        # Campos de entrada
        self.label_codigo = QLabel("Código:")
        self.edit_codigo = QLineEdit()
        self.edit_codigo.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
        self.label_nombre = QLabel("Nombre:")
        self.edit_nombre = QLineEdit()
        self.edit_nombre.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
        self.label_simbolo = QLabel("Símbolo:")
        self.edit_simbolo = QLineEdit()
        self.edit_simbolo.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
        self.label_factor_pago = QLabel("Factor Pago:")
        self.edit_factor_pago = QLineEdit()
        self.edit_factor_pago.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
        self.label_factor_inventario = QLabel("Factor Inventario:")
        self.edit_factor_inventario = QLineEdit()
        self.edit_factor_inventario.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
        self.label_tipo = QLabel("Tipo de Operador Cambiario:")
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Multiplicación", "División"])
        self.combo_tipo.setMinimumHeight(30)  # Establecer la altura mínima en 30 píxeles
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
        self.button_add = QPushButton("Añadir moneda")
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

        # Tabla de monedas
        self.table_monedas = QTableWidget()
        self.table_monedas.setColumnCount(3)
        self.table_monedas.setHorizontalHeaderLabels(["Código", "Nombre", "Símbolo"])
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
        input_layout.addWidget(self.label_simbolo)
        input_layout.addWidget(self.edit_simbolo)
        input_layout.addWidget(self.label_factor_pago)
        input_layout.addWidget(self.edit_factor_pago)
        input_layout.addWidget(self.label_factor_inventario)
        input_layout.addWidget(self.edit_factor_inventario)
        input_layout.addWidget(self.label_tipo)
        input_layout.addWidget(self.combo_tipo)
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

        self.button_add.setEnabled(False)
        self.button_modify.setEnabled(False)
        self.button_cancel.setEnabled(False)
        self.button_delete.setEnabled(False)

        self.button_add.setDisabled(True)
        self.button_modify.setDisabled(True)
        self.button_cancel.setDisabled(True)
        self.button_delete.setDisabled(True)

        self.buttons_enabled = False

        self.shortcut = QShortcut(Qt.CTRL + Qt.Key_D, self)
        self.shortcut.activated.connect(self.disabled_buttons)

        self.shortcut = QShortcut(Qt.CTRL + Qt.Key_H, self)
        self.shortcut.activated.connect(self.enable_buttons)

        return tab

    def enable_buttons(self):
        self.buttons_enabled = True
        self.button_add.setEnabled(True)
        self.button_modify.setEnabled(False)
        self.button_cancel.setEnabled(True)
        self.button_delete.setEnabled(False)

    def disabled_buttons(self):
        self.buttons_enabled = False
        self.button_add.setDisabled(True)
        self.button_modify.setDisabled(True)
        self.button_cancel.setDisabled(True)
        self.button_delete.setDisabled(True)

    def disable_input_fields(self):
        self.edit_codigo.setEnabled(False)
        self.edit_nombre.setEnabled(False)
        self.edit_simbolo.setEnabled(False)
        self.edit_factor_pago.setEnabled(False)
        self.edit_factor_inventario.setEnabled(False)
        self.combo_tipo.setEnabled(False)
        self.check_activo.setEnabled(False)
        self.check_activo.setChecked(False)

    def convertir_moneda(self, cantidad, moneda_origen, moneda_destino):
        # Consultar los factores de pago y inventario de las monedas
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT factor_pago, factor_inventario, tipo FROM monedas WHERE nombre = ?", (moneda_origen,))
        origen = cursor.fetchone()
        cursor.execute("SELECT factor_pago, factor_inventario, tipo FROM monedas WHERE nombre = ?", (moneda_destino,))
        destino = cursor.fetchone()
        conn.close()

        # Realizar la conversión según el tipo de operador cambiario
        if origen[2] == "Multiplicación":
            cantidad_convertida = cantidad * origen[0] * destino[0]
        else:
            cantidad_convertida = cantidad / origen[0] / destino[0]

        # Aplicar el factor de inventario si corresponde
        if destino[1] != 1:
            cantidad_convertida *= destino[1]

        return cantidad_convertida

    def add_moneda(self):
        self.is_new_moneda = True
        self.table_monedas.setEnabled(False)
        self.enable_input_fields()
        self.button_add.setText("Guardar cambios")
        self.button_add.clicked.disconnect(self.add_moneda)
        self.button_add.clicked.connect(self.save_new_moneda)

    def save_new_moneda(self):
        # Obtener los valores de los campos de entrada
        try:
            codigo = int(self.edit_codigo.text())
            if codigo <= 0:
                raise ValueError("El código debe ser un entero positivo")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
            return
        nombre = self.edit_nombre.text()
        simbolo = self.edit_simbolo.text()
        try:
            factor_pago = float(self.edit_factor_pago.text())
            factor_inventario = float(self.edit_factor_inventario.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Los valores de factor pago y factor inventario deben ser numéricos")
            return
        tipo = self.combo_tipo.currentText()
        activo = self.check_activo.isChecked()

        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Insertar la moneda en la base de datos
        cursor.execute("INSERT INTO monedas (codigom, nombre, simbolo, tipo, activo, factor_pago, factor_inventario) VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (codigo, nombre, simbolo, tipo, activo, factor_pago, factor_inventario))
        conn.commit()
        conn.close()

        # Agregar la moneda a la tabla
        row = self.table_monedas.rowCount()
        self.table_monedas.insertRow(row)
        self.table_monedas.setItem(row, 0, QTableWidgetItem(codigo))
        self.table_monedas.setItem(row, 1, QTableWidgetItem(nombre))
        self.table_monedas.setItem(row, 2, QTableWidgetItem(simbolo))

        # Limpiar los campos de entrada
        self.edit_codigo.clear()
        self.edit_nombre.clear()
        self.edit_simbolo.clear()
        self.edit_factor_pago.clear()
        self.edit_factor_inventario.clear()
        self.combo_tipo.setCurrentIndex(0)
        self.check_activo.setChecked(False)

        # Mostrar un mensaje de confirmación
        QMessageBox.information(self, "Moneda guardada", "La moneda ha sido guardada correctamente")

        # Deshabilitar los campos de entrada
        self.table_monedas.setEnabled(True)
        self.disable_input_fields()
        self.button_add.setText("Añadir moneda")
        self.button_add.clicked.disconnect(self.save_new_moneda)
        self.button_add.clicked.connect(self.add_moneda)
        self.is_new_moneda = False

    def enable_input_fields(self):
        self.edit_codigo.setEnabled(True)
        self.edit_nombre.setEnabled(True)
        self.edit_simbolo.setEnabled(True)
        self.edit_factor_pago.setEnabled(True)
        self.edit_factor_inventario.setEnabled(True)
        self.combo_tipo.setEnabled(True)
        self.check_activo.setEnabled(True)

    def cancel_moneda(self):
        self.table_monedas.setEnabled(True)
        self.edit_codigo.clear()
        self.edit_nombre.clear()
        self.edit_simbolo.clear()
        self.edit_factor_pago.clear()
        self.edit_factor_inventario.clear()
        self.combo_tipo.setCurrentIndex(0)
        self.check_activo.setChecked(False)
        self.disable_input_fields()
        self.button_modify.setText("Modificar")
        try:
            self.button_modify.clicked.disconnect(self.save_modified_moneda)
        except TypeError:
            pass
        self.button_modify.clicked.connect(self.modify_moneda)
        self.button_add.setText("Añadir moneda")
        try:
            self.button_add.clicked.disconnect(self.save_new_moneda)
        except TypeError:
            pass
        self.button_add.clicked.connect(self.add_moneda)

        # Refrescar la tabla para mostrar los cambios
        self.table_monedas.setRowCount(0)  # Limpiar la tabla
        self.load_moneda_data()  # Cargar los impuestos nuevamente

        self.is_new_moneda = False

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
        # Conectar a la base de datos
            conn = sqlite3.connect('Usuarios.db')
            cursor = conn.cursor()
            row = self.table_monedas.currentRow()
            if row != -1:
                try:
                    codigo = int(self.edit_codigo.text().strip())
                    if codigo <= 0:
                        raise ValueError("El código debe ser un entero positivo")
                except ValueError as e:
                    QMessageBox.warning(self, "Error", str(e))
                    return
                nombre = self.edit_nombre.text()
                simbolo = self.edit_simbolo.text()
                factor_pago = float(self.edit_factor_pago.text())
                factor_inventario = float(self.edit_factor_inventario.text())
                tipo = self.combo_tipo.currentText()
                activo = self.check_activo.isChecked()

                # Actualizar la moneda en la base de datos
                cursor.execute("UPDATE monedas SET nombre = ?, simbolo = ?, tipo = ?, activo = ?, factor_pago = ?, factor_inventario = ? WHERE codigom = ?",
                                (nombre, simbolo, tipo, activo, factor_pago, factor_inventario, codigo))
                conn.commit()
                conn.close()

                # Actualizar la tabla de monedas
                self.table_monedas.item(row, 0).setText(str(codigo))
                self.table_monedas.item(row, 1).setText(nombre)
                self.table_monedas.item(row, 2).setText(simbolo)

                # Mostrar un mensaje de confirmación
                QMessageBox.information(self, "Moneda modificada", "La moneda ha sido modificada correctamente")

                # Deshabilitar los campos de entrada
                self.table_monedas.setEnabled(True)
                self.disable_input_fields()
                self.button_modify.setText("Modificar")
                self.button_modify.clicked.connect(self.modify_moneda)

    def delete_moneda(self):
        row = self.table_monedas.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna moneda")
            return
        
        item = self.table_monedas.item(row, 1)  # Buscar el nombre de la moneda en la tabla
        if item is None:
            QMessageBox.warning(self, "Error", "No se ha seleccionado ninguna moneda")
            return
        
        nombre = item.text()

        # Preguntar al usuario si está seguro de eliminar
        confirm = QMessageBox.question(self, "Confirmar eliminación", 
                                        f"¿Estás seguro de que deseas eliminar la moneda: '{nombre}'?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.No:
            return  # Si el usuario selecciona "No", salir de la función
        
        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        
        # Eliminar la moneda de la base de datos
        cursor.execute("DELETE FROM monedas WHERE nombre = ?", (nombre,))
        conn.commit()
        conn.close()
        
        # Eliminar la fila de la tabla
        self.table_monedas.removeRow(row)
        
        # Actualizar la tabla de monedas
        self.load_moneda_data_into_table()
        
        # Mostrar un mensaje de confirmación
        QMessageBox.information(self, "Moneda eliminada", "La moneda ha sido eliminada correctamente")
        
        # Vaciar los campos de entrada
        self.edit_codigo.clear()
        self.edit_nombre.clear()
        self.edit_simbolo.clear()
        self.edit_factor_pago.clear()
        self.edit_factor_inventario.clear()
        self.combo_tipo.setCurrentIndex(0)
        self.check_activo.setChecked(False)
        self.disable_input_fields()

    def load_moneda_data(self):
        # Conectar a la base de datos
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
                    simbolo = item.text()
                # Cargar los datos de la moneda en los campos de entrada
                self.edit_codigo.setText(codigo)
                self.edit_nombre.setText(nombre)
                self.edit_simbolo.setText(simbolo)
                self.edit_factor_pago = float(self.edit_factor_pago.text())
                self.edit_factor_inventario = float(self.edit_factor_inventario.text())
            else:
                # Vaciar los campos de entrada cuando no se haya seleccionado ninguna moneda
                self.edit_codigo.clear()
                self.edit_nombre.clear()
                self.edit_simbolo.clear()
                self.edit_factor_pago.clear()
                self.edit_factor_inventario.clear()
                self.combo_tipo.setCurrentIndex(0)
                self.disable_input_fields()

        # Consultar las monedas en la base de datos
        cursor.execute("SELECT codigom, nombre, simbolo, activo, factor_pago, factor_inventario FROM monedas")
        monedas = cursor.fetchall()

        # Agregar las monedas a la tabla
        self.table_monedas.setRowCount(0)  # Limpiar la tabla
        for row, moneda in enumerate(monedas):
            self.table_monedas.insertRow(row)
            self.table_monedas.setItem(row, 0, QTableWidgetItem(str(moneda[0])))  # Mostrar el código
            self.table_monedas.setItem(row, 1, QTableWidgetItem(moneda[1]))  # Mostrar el nombre
            self.table_monedas.setItem(row, 2, QTableWidgetItem(moneda[2]))  # Mostrar el símbolo

        conn.close()

    def load_moneda_data_into_table(self):
        # Conectar a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()

        # Consultar las monedas en la base de datos
        cursor.execute("SELECT codigom, nombre, simbolo, activo FROM monedas")
        monedas = cursor.fetchall()

        # Limpiar la tabla
        self.table_monedas.setRowCount(0)

        # Agregar las monedas a la tabla
        for row, moneda in enumerate(monedas):
            self.table_monedas.insertRow(row)
            self.table_monedas.setItem(row, 0, QTableWidgetItem(str(moneda[0])))  # Mostrar el códigom
            self.table_monedas.setItem(row, 1, QTableWidgetItem(moneda[1]))  # Mostrar el nombre
            self.table_monedas.setItem(row, 2, QTableWidgetItem(moneda[2]))  # Mostrar el símbolo

            # Agregar el checkbox a la tabla
            checkbox = QCheckBox()
            checkbox.setChecked(moneda[3] == 1)  # Establecer el estado del checkbox
            self.table_monedas.setCellWidget(row, 3, checkbox)  # Agregar el checkbox a la celda

        conn.close()

    def load_selected_moneda(self):
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
                    simbolo = item.text()
                # Cargar los datos de la moneda en los campos de entrada
                self.edit_codigo.setText(codigo)
                self.edit_nombre.setText(nombre)
                self.edit_simbolo.setText(simbolo)

                # Consultar el tipo, estado, factor_pago y factor_inventario de la moneda en la base de datos
                conn = sqlite3.connect('Usuarios.db')
                cursor = conn.cursor()

                cursor.execute("SELECT tipo, activo, factor_pago, factor_inventario FROM monedas WHERE nombre = ?", (nombre,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    tipo, factor_pago, factor_inventario, activo = result
                    self.combo_tipo.setCurrentText(tipo)
                    self.check_activo.setChecked(bool(activo))
                    self.edit_factor_pago.setText(str(factor_pago))
                    self.edit_factor_inventario.setText(str(factor_inventario))
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
            self.combo_tipo.setEnabled(False)
            self.check_activo.setEnabled(False)
            self.check_activo.setChecked(False)
            self.button_modify.setEnabled(False)
            self.button_add.setEnabled(self.buttons_enabled)
            self.button_delete.setEnabled(False)
        else:
            # Si hay una selección, habilita los botones solo si están permitidos
            self.button_modify.setEnabled(self.buttons_enabled)
            self.button_add.setEnabled(False)
            self.button_delete.setEnabled(self.buttons_enabled)

    def create_columns(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(monedas)")
        columns = [t[1] for t in cursor.fetchall()]
        if 'factor_pago' not in columns:
            cursor.execute("ALTER TABLE monedas ADD COLUMN factor_pago REAL")
        if 'factor_inventario' not in columns:
            cursor.execute("ALTER TABLE monedas ADD COLUMN factor_inventario REAL")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = Monedas()
    config.show()
    sys.exit(app.exec_())