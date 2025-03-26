import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QAbstractItemView, QLabel, QTableWidget, QStatusBar, QTableWidgetItem, QHeaderView, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
import sqlite3

conn = sqlite3.connect("Usuarios.db")  
cursor = conn.cursor()

class VentanaDepositos(QMainWindow):
    deposito_seleccionado = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.statusbar = QStatusBar()
        self.statusbar.setFixedHeight(25)

        self.setWindowTitle("Depositos")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon("icono.png"))

        # Crear el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear el layout principal
        layout = QVBoxLayout()

        # Crear la barra de búsqueda
        search_label = QtWidgets.QLabel("Buscar Deposito")

        # Cambiar el tipo de letra del QLabel
        font = QtGui.QFont("Montserrat SemiBold", 9, QtGui.QFont.Bold)  # Fuente Arial, tamaño 14, negrita
        search_label.setFont(font)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar deposito")
        self.search_input.setStyleSheet("QLineEdit {\n"
        "                background-color: #ffffff; /* Color de fondo blanco */\n"
        "                border: 1px solid #ccc; /* Borde gris claro */\n"
        "                border-radius: 5px; /* Radio del borde */\n"
        "                padding: 5px; /* Relleno */\n"
        "                color: #000000; /* Color del texto negro */\n"
        "            }")
        self.search_input.setFixedWidth(300)
        self.search_input.textChanged.connect(self.filtrar_productos)


        layout.addWidget(search_label)
        layout.addWidget(self.search_input)

        # Crear la tabla
        self.table = QtWidgets.QTableWidget()
        self.table.setStyleSheet("""
                    QTableWidget {
                    gridline-color: transparent;  /* Oculta todas las líneas de la cuadrícula */
                    }
                    QTableWidget::item {
                        border-right: 1px solid #ccc;  /* Línea vertical entre columnas */
                    }
                    QTableWidget::item:last {
                        border-right: none;  /* Elimina la línea vertical de la última columna */
                    }
                    QTableWidget::item:selected {
                        background-color: #1bb0b0; /* Color de fondo de la fila seleccionada */
                        color: #ffffff; /* Color del texto de la fila seleccionada */
                    }
                    QHeaderView::section {
                        background-color: #1bb0b0; /* Color cuando se coloca el cursor sobre el encabezado */
                        border: 5px;
                        color: #ffffff;
            }
        """)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Codigo", "Descripción"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)



        layout.addWidget(self.table)
        layout.addWidget(self.statusbar)

        self.cargar_depositos()

        # Conectar el evento de doble clic en la tabla
        self.table.doubleClicked.connect(self.on_table_double_click)

        # Establecer el layout al widget central
        central_widget.setLayout(layout)

    def on_table_double_click(self, index):
        # Obtener el código y el nombre del depósito seleccionado
        codigo = self.table.item(index.row(), 0).text()
        nombre = self.table.item(index.row(), 1).text()

        # Emitir la señal con los datos del depósito
        self.deposito_seleccionado.emit(codigo, nombre)

        # Cerrar la ventana
        self.close()

    def filtrar_productos(self):
        texto_busqueda = self.search_input.text().lower()
        for fila in range(self.table.rowCount()):
            # Obtener el texto de cada celda
            codigo = self.table.item(fila, 0).text().lower()
            descripcion = self.table.item(fila, 1).text().lower()

            # Comprobar si el texto de búsqueda está en el código o descripción
            if texto_busqueda in codigo or texto_busqueda in descripcion:
                self.table.showRow(fila)  # Mostrar la fila si coincide
            else:
                self.table.hideRow(fila)  # Ocultar la fila si no coincide

    def cargar_depositos(self):
        # Abrir la conexión a la base de datos
        self.conn = sqlite3.connect('Usuarios.db')
        self.cursor = conn.cursor()

        # Carga el deposito desde la base de datos
        cursor.execute("SELECT codigo, nombre FROM depositos")
        depositos = cursor.fetchall()

        self.table.setRowCount(0)  # Limpiar la tabla

        # Llenar la tabla con los depositos
        for row_number, row_data in enumerate(depositos):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        # Cerrar la conexión a la base de datos
        self.cursor.close()
        self.conn.close()

        # Actualiza la barra de estado con la cantidad de marcas creadas
        self.statusbar.showMessage(f"Productos creados: {len(depositos)}")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = VentanaDepositos()
    mainwindow.show()
    sys.exit(app.exec_())