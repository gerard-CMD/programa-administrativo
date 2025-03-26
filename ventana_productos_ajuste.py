import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QLabel, QAbstractItemView, QTableWidget, QStatusBar, QTableWidgetItem, QHeaderView, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal
import sqlite3

conn = sqlite3.connect("Usuarios.db")  
cursor = conn.cursor()

class InventoryWindowAjuste(QMainWindow):
    def __init__(self, ventana_cargar=None, fila_actual=None):
        super().__init__()
        self.ventana_cargar = ventana_cargar
        self.costos_productos = {}
        self.fila_actual = fila_actual

        self.statusbar = QStatusBar()
        self.statusbar.setFixedHeight(25)

        self.setWindowTitle("ZISCON ADMINISTRATIVO (V 1.0)")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon("icono.png"))

        self.imagen_productos= QLabel(self)
        pixmap = QPixmap("PRODUCTOS_INV.png")
        self.imagen_productos.setPixmap(pixmap)
        self.imagen_productos.setGeometry(QtCore.QRect(320, 10, 780, 60))
        self.imagen_productos.show()
 
        # Crear el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear el layout principal
        layout = QVBoxLayout()

        # Crear la barra de búsqueda
        search_label = QtWidgets.QLabel("Buscar Producto")

        # Cambiar el tipo de letra del QLabel
        font = QtGui.QFont("Montserrat SemiBold", 9, QtGui.QFont.Bold)  # Fuente Arial, tamaño 14, negrita
        search_label.setFont(font)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar producto")
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
                        background-color: #008080; /* Color cuando se coloca el cursor sobre el encabezado */
                        border: 5px;
                        color: #ffffff;
            }
        """)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Codigo", "Descripción", "Referencia"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)

        layout.addWidget(self.table)
        layout.addWidget(self.statusbar)

        self.table.itemDoubleClicked.connect(self.cargar_producto_en_fila_actual)

        self.cargar_productos()

        # Establecer el layout al widget central
        central_widget.setLayout(layout)

    def filtrar_productos(self):
        texto_busqueda = self.search_input.text().lower()
        for fila in range(self.table.rowCount()):
            # Obtener el texto de cada celda
            codigo = self.table.item(fila, 0).text().lower()
            descripcion = self.table.item(fila, 1).text().lower()
            referencia = self.table.item(fila, 2).text().lower()

            # Comprobar si el texto de búsqueda está en el código o descripción
            if texto_busqueda in codigo or texto_busqueda in descripcion or texto_busqueda in referencia:
                self.table.showRow(fila)  # Mostrar la fila si coincide
            else:
                self.table.hideRow(fila)  # Ocultar la fila si no coincide

    def cargar_producto_en_ventana_cargar(self, item):
        # Obtener el código del producto seleccionado
        codigo = self.table.item(item.row(), 0).text()
        
        # Abrir la conexión a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        
        # Cargar los datos del producto desde la base de datos
        cursor.execute("SELECT descripcion, costo_actual, costo_actual_referencial FROM productos_inventario WHERE codigo = ?", (codigo,))
        producto = cursor.fetchone()
        
        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()
        
        # Cargar los datos del producto en la ventana CargarProductos
        if producto:
            if self.ventana_cargar is not None:  # Verifica si la ventana CargarProductos existe
                if hasattr(self.ventana_cargar, 'tabla_productos'):  # Verifica si la ventana CargarProductos tiene el atributo tabla_productos
                    # Buscar la primera fila vacía
                    fila_vacia = 0
                    while fila_vacia < self.ventana_cargar.tabla_productos.rowCount():
                        if self.ventana_cargar.tabla_productos.item(fila_vacia, 0) is None or self.ventana_cargar.tabla_productos.item(fila_vacia, 0).text() == '':
                            break
                        fila_vacia += 1

                    # Si no hay filas vacías, agregar una nueva fila
                    if fila_vacia >= self.ventana_cargar.tabla_productos.rowCount():
                        self.ventana_cargar.tabla_productos.insertRow(fila_vacia)

                    # Cargar los datos en la fila vacía
                    self.ventana_cargar.tabla_productos.setItem(fila_vacia, 0, QtWidgets.QTableWidgetItem(codigo))
                    self.ventana_cargar.tabla_productos.setItem(fila_vacia, 1, QtWidgets.QTableWidgetItem(producto[0]))
                    self.ventana_cargar.tabla_productos.setRowHeight(fila_vacia, 35)
                    self.ventana_cargar.tabla_productos.setCurrentCell(fila_vacia, 3)  # Posicionar el cursor en la columna 3
                    self.ventana_cargar.tabla_productos.editItem(self.ventana_cargar.tabla_productos.item(fila_vacia, 3))  # Editar la celda automáticamente
        # Cerrar la ventana
        self.close()

    def cargar_productos(self):
        # Abrir la conexión a la base de datos
        self.conn = sqlite3.connect('Usuarios.db')
        self.cursor = conn.cursor()

        # Carga los productos desde la base de datos
        cursor.execute("SELECT codigo, descripcion, codigo_barra FROM productos_inventario")
        productos = cursor.fetchall()

        self.table.setRowCount(0)  # Limpiar la tabla

        # Llenar la tabla con los productos
        for row_number, row_data in enumerate(productos):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        # Cerrar la conexión a la base de datos
        self.cursor.close()
        self.conn.close()

        # Actualiza la barra de estado con la cantidad de marcas creadas
        self.statusbar.showMessage(f"Productos creados: {len(productos)}")

    def cargar_producto_en_fila_actual(self, item):
        # Obtener el código del producto seleccionado
        codigo = self.table.item(item.row(), 0).text() if self.table.item(item.row(), 0) else None

        if codigo is None:
            print("Error: No se pudo obtener el código del producto.")
            return
        
        # Abrir la conexión a la base de datos
        conn = sqlite3.connect('Usuarios.db')
        cursor = conn.cursor()
        
        # Cargar los datos del producto desde la base de datos
        cursor.execute("""
            SELECT p.descripcion, e.cantidad, p.costo_actual_referencial
            FROM productos_inventario p
            JOIN existencia_productos e ON p.codigo = e.codigo
            WHERE p.codigo = ?
        """, (codigo,))

        producto = cursor.fetchone()

        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()

        if producto:
            # Verificar si el producto ya está en la fila actual
            if self.ventana_cargar.tabla_productos.item(self.fila_actual, 0) is not None:
                existing_codigo = self.ventana_cargar.tabla_productos.item(self.fila_actual, 0).text()
                if existing_codigo == codigo:
                    print("El producto ya está en la fila actual.")
                    return  # No agregar el producto si ya está
                
                # Buscar la primera fila vacía
                fila_vacia = self.encontrar_fila_vacia()
                if fila_vacia is not None:
                    self.fila_actual = fila_vacia  # Actualizar la fila actual a la fila vacía
                
            # Cargar el producto en la fila actual de CargarProductos
            self.ventana_cargar.tabla_productos.setItem(self.fila_actual, 0, QtWidgets.QTableWidgetItem(codigo))
            self.ventana_cargar.tabla_productos.setItem(self.fila_actual, 1, QtWidgets.QTableWidgetItem(producto[0]))
            self.ventana_cargar.tabla_productos.setItem(self.fila_actual, 4, QtWidgets.QTableWidgetItem(str(producto[1])))

            # Crear un QTableWidgetItem para el costo, pero no lo mostramos
            costo_item = QtWidgets.QTableWidgetItem()
            costo_item.setData(QtCore.Qt.UserRole, producto[2])  # Almacena el costo en el UserRole
            self.ventana_cargar.tabla_productos.setItem(self.fila_actual, 2, costo_item)  # Puedes usar la columna 2 para almacenar el costo

            self.ventana_cargar.tabla_productos.setRowHeight(self.fila_actual, 35)
            self.ventana_cargar.tabla_productos.setCurrentCell(self.fila_actual, 3)  # Posicionar el cursor en la columna 3
            self.ventana_cargar.tabla_productos.editItem(self.ventana_cargar.tabla_productos.item(self.fila_actual, 3))  # Editar la celda automáticamente
            self.close()  # Cierra la ventana de inventario después de cargar el producto
        else:
            print("Error: Producto no encontrado en la base de datos.")

    def encontrar_fila_vacia(self):
        for fila in range(self.ventana_cargar.tabla_productos.rowCount()):
            if self.ventana_cargar.tabla_productos.item(fila, 0) is None or self.ventana_cargar.tabla_productos.item(fila, 0).text() == '':
                return fila
        return None  # Si no hay filas vacías

    def filtrar_productos_por_codigo(self, codigo):
        # Obtener la lista de productos
        productos = self.obtener_productos()
        
        # Filtrar los productos que se asemejan al código
        productos_similares = [producto for producto in productos if codigo in producto[0]]
        
        # Mostrar los productos similares en la tabla
        self.mostrar_productos_similares(productos_similares)

    def obtener_productos(self):
        # Obtener la lista de productos desde la base de datos
        cursor.execute("SELECT codigo, descripcion, codigo_barra FROM productos_inventario")
        productos = cursor.fetchall()
        return productos

    def mostrar_productos_similares(self, productos):
        # Limpiar la tabla
        self.table.setRowCount(0)
        
        # Mostrar los productos similares en la tabla
        for row_number, row_data in enumerate(productos):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = InventoryWindowAjuste()
    mainwindow.show()
    sys.exit(app.exec_())