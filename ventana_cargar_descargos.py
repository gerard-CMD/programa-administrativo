import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QVBoxLayout, QLineEdit, QLabel, QAbstractItemView, QTableWidget, QStatusBar, QTableWidgetItem, QHeaderView, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
import sqlite3

conn = sqlite3.connect("Usuarios.db")  
cursor = conn.cursor()

class VentanaCargarTransaccionDescargo(QMainWindow):
    def __init__(self, cargar_productos_instance, ventana_cargar_transaccion=None,):
        super().__init__()
        self.ventana_cargar_transaccion = ventana_cargar_transaccion
        self.cargar_productos_instance = cargar_productos_instance  # Guarda la referencia

        self.statusbar = QStatusBar()
        self.statusbar.setFixedHeight(25)

        self.setWindowTitle("Transacciones Descargos")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon("icono.png"))
 
        # Crear el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear el layout principal
        layout = QVBoxLayout()

        # Crear la barra de búsqueda
        self.transacciones_combobox = QComboBox()
        self.transacciones_combobox.setMaximumWidth(150)
        self.transacciones_combobox.addItem("Guardadas")
        self.transacciones_combobox.addItem("Procesadas")
        self.transacciones_combobox.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                font-family: Arial;
            }
            QComboBox::item:selected {
                background-color: #1bb0b0; /*
                color: #ffffff; /* Texto blanco cuando se selecciona un item */
            }
        """)

        layout.addWidget(self.transacciones_combobox)

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
                        background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */
                        border: 5px;
                        color: #ffffff;
            }
        """)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Número de Operación", "Fecha de Operación", "Estado"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        layout.addWidget(self.table)
        layout.addWidget(self.statusbar)

        self.table.itemDoubleClicked.connect(self.on_double_click)

        self.cargar_operaciones_guardadas()

        # Establecer el layout al widget central
        central_widget.setLayout(layout)

    def cargar_operaciones_guardadas(self):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        
        # Cargar solo el número de operación y la fecha
        cursor.execute('SELECT numero_operacion, fecha, estado FROM operaciones_descargas_guardadas ORDER BY fecha DESC;')
        operaciones = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)  # Limpiar la tabla antes de cargar
        for operacion in operaciones:
            row_position = self.table.rowCount() 
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(operacion[0])))  # Número de operación
            self.table.setItem(row_position, 1, QTableWidgetItem(operacion[1]))  # Fecha
            self.table.setItem(row_position, 2, QTableWidgetItem(operacion[2]))  # Estado

        # Actualiza la barra de estado con la cantidad de registros creados
        self.statusbar.showMessage(f"Registros: {len(operaciones)}")

    def on_double_click(self, item):
        row = item.row()
        numero_operacion = self.table.item(row, 0).text()  # Número de operación

        # Cargar los productos asociados a la operación
        self.cargar_productos_por_operacion(numero_operacion)

        self.close()

    def cargar_productos_por_operacion(self, numero_operacion):
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        
        # Obtener los productos asociados a la operación
        cursor.execute('SELECT codigo, cantidad FROM operaciones_descargas_guardadas WHERE numero_operacion = ?', (numero_operacion,))
        productos = cursor.fetchall()
        conn.close()

        # Imprimir los productos para verificar que se están recuperando correctamente
        print(productos)

        # Buscar la primera fila vacía
        row_position = 0
        while row_position < self.cargar_productos_instance.tabla_productos.rowCount():
            item = self.cargar_productos_instance.tabla_productos.item(row_position, 0)  # Verificar la columna 0 (código)
            if item is None or item.text() == '':  # Si la celda está vacía
                break  # Usar esta fila
            row_position += 1

        # Cargar los productos en la tabla de productos
        for producto in productos:
            if row_position >= self.cargar_productos_instance.tabla_productos.rowCount():
                self.cargar_productos_instance.tabla_productos.insertRow(row_position)
        
            # Asumiendo que la columna 0 es el código y la columna 1 es la cantidad
            self.cargar_productos_instance.tabla_productos.setItem(row_position, 0, QTableWidgetItem(producto[0]))  # Código
            self.cargar_productos_instance.tabla_productos.setItem(row_position, 3, QTableWidgetItem(str(producto[1])))  # Cantidad
            row_position += 1

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = VentanaCargarTransaccionDescargo()
    mainwindow.show()
    sys.exit(app.exec_())