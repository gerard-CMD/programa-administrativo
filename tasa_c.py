import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtWidgets, QtGui, QtCore
import requests
import math
from bs4 import BeautifulSoup
import datetime
from PyQt5.QtWidgets import QComboBox, QHeaderView, QAbstractItemView
import sqlite3

class MoneyLineEdit(QLineEdit):
    def __init__(self):
        super(MoneyLineEdit, self).__init__()
        self.setText('0.00')
        self.setCursorPosition(4)  # Posición del cursor al final de la cadena

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left or event.key() == Qt.Key_Right:
            super(MoneyLineEdit, self).keyPressEvent(event)
        elif event.key() == Qt.Key_Backspace:
            text = self.text()
            if len(text) > 4:
                self.setText(text[:-1])
            else:
                self.setText('0.00')
            self.setCursorPosition(len(self.text()))
        else:
            text = self.text()
            if event.text().isdigit():
                if '.' in text:
                    parts = text.split('.')
                    integer_part = parts[0]
                    decimal_part = parts[1]
                    if len(decimal_part) < 2:
                        self.setText(integer_part + '.' + decimal_part + event.text())
                        self.setCursorPosition(len(integer_part) + 3)
                    else:
                        integer_part = str(int(integer_part + event.text()))
                        self.setText(decimal_part + '.' + integer_part)
                        self.setCursorPosition(len(integer_part) + 1)
                else:
                    integer_part = str(int(text + event.text()))
                    self.setText(integer_part + '.00')
                    self.setCursorPosition(len(integer_part) + 1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZISCON ADMINISTRATIVO (V 1.0)")
        self.setGeometry(100, 100, 750, 400)
        self.setWindowIcon(QIcon("icono.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Crear la tabla
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)  # Número de columnas
        self.table_widget.setHorizontalHeaderLabels([
        "Nombre", "Símbolo", "Ult. Factor Pago", "Ult. Factor Inv", "Ult. Fecha", "Factor Unico", "Factor Pago", "Factor Inv"
        ])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_widget.setStyleSheet("QTableWidget::item:selected {\n"
        "                background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */\n"
        "                color: white; /* Color del texto de la fila seleccionada */\n"
        "            }\n"
        "            QHeaderView::section {\n"
        "                background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */\n"
        "                border: 5px;\n"
        "                color: #ffffff;\n"
        "            }")
        self.table_widget.verticalHeader().setVisible(False)

        # Agregar datos de ejemplo
        self.table_widget.setRowCount(1)
        self.table_widget.setItem(0, 0, QTableWidgetItem("Dólar"))
        self.table_widget.setItem(0, 1, QTableWidgetItem("$"))

        # Deshabilitar edición en las primeras 5 columnas
        for i in range(5):
            self.table_widget.setItem(0, i, QTableWidgetItem(""))
            item = self.table_widget.item(0, i)
            item.setFlags(Qt.ItemIsEnabled)  # Solo permite selección, no edición

        # Hacer las últimas 3 columnas editables
        for i in range(5, 8):
            self.table_widget.setColumnWidth(i, 100) # Ajustar ancho de columnas editables
            item = QTableWidgetItem("0.00")
            item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.table_widget.setItem(0, i, item)

        # Conectar el doble clic a la función para saltar a la columna 6
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        self.layout.addWidget(self.table_widget)

        self.actualizar_button = QPushButton('Actualizar')
        self.actualizar_button.setFixedWidth(100)
        self.actualizar_button.setStyleSheet("""
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
        self.actualizar_button.clicked.connect(self.update_rates)

        # Crear layout horizontal para el botón de salir
        exit_layout = QHBoxLayout()
        exit_layout.addStretch()  # Agregar un estirador para empujar el botón hacia la derecha
        exit_layout.addWidget(self.actualizar_button)

        # Agregar el layout horizontal al layout vertical
        self.layout.addLayout(exit_layout)

        #self.show()

        self.conn = sqlite3.connect('Usuarios.db')  # Conectar a la base de datos
        self.cursor = self.conn.cursor()
        self.load_moneda_data()  # Cargar datos de monedas desde la base de datos

    def update_rates(self):
        # Realizar solicitud HTTP a la página del Banco Central
        url = "https://www.bcv.org.ve/"  # URL de la página del Banco Central
        response = requests.get(url)

        # Parsear el contenido de la página con BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extraer la tasa de cambio actual de la página document.querySelector
        rate_element = soup.select_one("#dolar > div > div > div.col-sm-6.col-xs-6.centrado")
        rate_text = rate_element.text.strip()  # Texto de la tasa de cambio
        rate_value = float(rate_text.replace(',', '.'))  # Valor de la tasa de cambio
        if rate_value * 100 % 10 >= 5:
            rate_value = math.ceil(rate_value * 100) / 100  # Redondear hacia arriba

        # Actualizar solo la moneda "Dolares" en la base de datos
        for row in range(self.table_widget.rowCount()):
            if self.table_widget.item(row, 0).text() == "Dolares":
                # Guardar el valor anterior en la columna "Último Factor Pago" y "Último Factor Inventario"
                ultimo_factor_pago = self.table_widget.item(row, 6).text()
                ultimo_factor_inventario = self.table_widget.item(row, 7).text()

                # Actualizar la columna "Factor Pago" y "Factor Inventario" con el nuevo valor
                self.table_widget.item(row, 6).setText("{:.2f}".format(round(rate_value, 2)))  # Factor Pago
                self.table_widget.item(row, 7).setText("{:.2f}".format(round(rate_value, 2)))  # Factor Inventario

                # Actualizar la columna "Último Factor Pago" y "Último Factor Inventario" con el valor anterior
                self.table_widget.item(row, 2).setText(ultimo_factor_pago)  # Último Factor Pago
                self.table_widget.item(row, 3).setText(ultimo_factor_inventario)  # Último Factor Inventario

                # Actualizar la base de datos
                self.cursor.execute("UPDATE monedas SET factor_pago = ?, factor_inventario = ?, ultimo_factor_pago = ?, ultimo_factor_inventario = ? WHERE nombre = ?", 
                                    (round(rate_value, 2), round(rate_value, 2), ultimo_factor_pago, ultimo_factor_inventario, "Dolares"))
                self.conn.commit()  # Confirmar los cambios en la base de datos
                break

    def load_moneda_data(self):
        self.cursor.execute("SELECT nombre, simbolo, factor_pago, factor_inventario, fecha_ultimo_cambio, ultimo_factor_pago, ultimo_factor_inventario FROM monedas")
        rows = self.cursor.fetchall()
        self.table_widget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table_widget.setItem(i, 0, QTableWidgetItem(row[0]))  # Nombre
            self.table_widget.setItem(i, 1, QTableWidgetItem(row[1]))  # Símbolo
            self.table_widget.setItem(i, 6, QTableWidgetItem(str(row[2])))  # Factor Pago
            self.table_widget.setItem(i, 7, QTableWidgetItem(str(row[3])))  # Factor Inventario
            self.table_widget.setItem(i, 4, QTableWidgetItem(row[4]))  # Fecha de último cambio
            self.table_widget.setItem(i, 2, QTableWidgetItem(str(row[5])))  # Último Factor Pago
            self.table_widget.setItem(i, 3, QTableWidgetItem(str(row[6])))  # Último Factor Inventario

    def closeEvent(self, event):
        self.conn.close()  # Cerrar la conexión a la base de datos cuando se cierra la ventana
        event.accept()

    def on_cell_double_clicked(self, row, column):
        if column < 5:
            self.table_widget.setCurrentCell(row, 5) # Salta a la columna 6
            # Crea una instancia de MoneyLineEdit
            money_line_edit = MoneyLineEdit()
            self.table_widget.setCellWidget(row, 5, money_line_edit)
            # Selecciona la celda y la hace editable
            item = self.table_widget.item(row, 5)
            item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            # Asigna el foco a la celda para que se pueda escribir directamente
            self.table_widget.editItem(item)
        elif column == 5:  # Agregamos esta condición para crear MoneyLineEdit en columna 6
            money_line_edit = MoneyLineEdit()
            item = QTableWidgetItem("")  # Crea un objeto QTableWidgetItem
            self.table_widget.setCellWidget(row, 5, money_line_edit)
            self.table_widget.setItem(row, 5, item)  # Asigna el objeto QTableWidgetItem
            money_line_edit.editingFinished.connect(self.update_factor_unico)  # Conecta la señal editingFinished
            self.table_widget.editItem(item)  # Llama a editItem con el objeto QTableWidgetItem

    def update_factor_unico(self):
        row = self.table_widget.currentRow()
        money_line_edit = self.table_widget.cellWidget(row, 5)
        if money_line_edit is not None:
            factor_unico = money_line_edit.text()
            nombre = self.table_widget.item(row, 0).text()  # Obtener el nombre de la moneda
            fecha_actual = datetime.date.today().isoformat()  # Obtener la fecha actual

            # Obtener los valores actuales de factor_pago y factor_inventario
            self.cursor.execute("SELECT factor_pago, factor_inventario FROM monedas WHERE nombre = ?", (nombre,))
            row = self.cursor.fetchone()
            factor_pago_actual = row[0]
            factor_inventario_actual = row[1]

            # Actualizar la tabla con el nuevo factor único y los valores anteriores
            self.cursor.execute("UPDATE monedas SET factor_pago = ?, factor_inventario = ?, fecha_ultimo_cambio = ?, factor_unico = ?, ultimo_factor_pago = ?, ultimo_factor_inventario = ? WHERE nombre = ?", (factor_unico, factor_unico, fecha_actual, factor_unico, factor_pago_actual, factor_inventario_actual, nombre))
            self.conn.commit()  # Confirmar los cambios en la base de datos
            self.load_moneda_data()  # Recargar los datos de la tabla para reflejar los cambios

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())