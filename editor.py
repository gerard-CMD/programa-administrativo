from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QIcon
import chardet

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor ZISCON-CODE")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon("icono.png"))  # Agrega el icono a la ventana

        self.editor = QsciScintilla()
        self.setCentralWidget(self.editor)

        # Configurar el resaltador de sintaxis para Python
        lexer = QsciLexerPython()
        self.editor.setLexer(lexer)

        # Cargar un archivo de código al iniciar
        self.load_file()

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            try:
                # Detectar la codificación
                with open(file_name, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']

                # Abrir el archivo con la codificación detectada
                with open(file_name, 'r', encoding=encoding) as f:
                    self.editor.setText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo: {e}")

if __name__ == "__main__":
    app = QApplication([])
    editor = Editor()
    editor.show()
    app.exec_()