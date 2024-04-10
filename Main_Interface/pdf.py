import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
import fitz
class PDFView(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_path = "test.pdf"#pdf path
        self.text_edit = QTextEdit()
        self.extract_text()
        self.setup_ui()

    def extract_text(self):
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.text_edit.setPlainText(text)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        self.text_edit.setStyleSheet("background-color:white;")
        self.text_edit.setAlignment(Qt.AlignCenter)
class InfoLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.information=QLabel("Info Appears here")
        self.information.setStyleSheet("color: white;")
        self.information.setStyleSheet("""background-color:#564F6F;
                                       """)
        self.information.setAlignment(Qt.AlignCenter)

class ButtonHolder(QWidget):
    def __init__(self):
        super().__init__()
        #All The Buttons
        self.setFixedSize(120,600)
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet("background-color:#564F6F")
        self.button_1=QPushButton()
        self.button_1.setText("Meaning")
        self.button_1.setFixedSize(100, 40)
        self.button_1.setStyleSheet("border-radius: 10px;")
        self.button_2=QPushButton()
        self.button_2.setText("Homonym")
        self.button_2.setFixedSize(100, 40)
        self.button_2.setStyleSheet("border-radius: 10px;")
        self.button_3=QPushButton()
        self.button_3.setText("Dictonary")
        self.button_3.setFixedSize(100, 40)
        self.button_3.setStyleSheet("border-radius: 10px;")
        self.container=QVBoxLayout()
        self.container.addWidget(self.button_1)
        self.container.addWidget(self.button_2)
        self.container.addWidget(self.button_3)
        self.container.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.container)
        


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 PDF Viewer")
        self.resize(800, 600)
        self.pdf_view=PDFView()
        self.information=InfoLabel()
        self.button_holder=ButtonHolder()
        #Layout
        self.qlayout=QVBoxLayout()
        self.qlayout.addWidget(self.pdf_view.text_edit,10)
        self.qlayout.addWidget(self.information.information,1)
        self.hlayout=QHBoxLayout()
        self.hlayout.addLayout(self.qlayout)
        self.hlayout.addWidget(self.button_holder)
        self.hlayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.hlayout)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(""" 
    QWidget{
            background-color:#564F6F;
    }              
    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: #333333;
    }
    QPushButton {
        font-size: 14px;
        font-weight: bold;
        color: #ffffff;
        background-color: #564F6F;
        border: 1px solid black;             
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #444444;
    }
    QPushButton:pressed {
        background-color: #555555;
    }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())