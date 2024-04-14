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
    QTextEdit,
    QLineEdit,
    QSlider
)
from PySide6.QtCore import Qt, QTimer # Added QTextCursor import
import fitz
import extra_functions
from PySide6 import QtGui
from PySide6.QtGui import QTextBlockFormat, QFont, QTextCursor 

class CustomButton(QPushButton):
    def __init__(self, label):
        super().__init__()
        font = QFont()
        font.setFamilies([u"JetBrains Mono NL"])
        font.setBold(True)
        self.setFont(font)
        self.setText(label)
        self.setFixedSize(120, 40)  # Adjust the size as needed
        self.setStyleSheet("""
            QPushButton {
                background-color:  #353535;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #282828;
            }
            QPushButton:pressed {
                background-color: #4c4c4c;
            }
        """)

class PDFView(QWidget):
    def __init__(self, path):
        super().__init__()
        self.pdf_path = path
        self.text_edit = QTextEdit()
        self.extract_text()
        self.setup_ui()

    def extract_text(self):
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.text_edit.setPlainText(text)
        # Center align the text
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignCenter)
        cursor.mergeBlockFormat(block_format)
        self.text_edit.setTextCursor(cursor)
        # Set cursor position to the beginning of the text
        self.text_edit.moveCursor(QtGui.QTextCursor.Start)

    def setup_ui(self):
        self.text_edit.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

    def get_selected_text(self):
        return self.text_edit.textCursor().selectedText()


class InfoLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.information = QLabel("Info Appears here")
        self.information.setMaximumHeight(100)
        self.information.setStyleSheet("""background-color:#d7d7d7;
                                         border-radius: 15px;
                                       """)

    def print_data(self, message):
        self.information.setText(message)


class ButtonHolder(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.meaning_button = CustomButton("Meaning")
        self.meaning_button.clicked.connect(self.on_meaning_button_clicked)

        self.synonym_button = CustomButton("Synonym")
        self.synonym_button.clicked.connect(self.on_synonym_button_clicked)

        self.speech_button = CustomButton("Read Aloud")
        self.speech_button.clicked.connect(self.on_speech_button_clicked)
        
        self.auto_scroll_button = CustomButton("Auto-Scroll")
        self.auto_scroll_button.setCheckable(True)
        self.auto_scroll_button.toggled.connect(self.on_auto_scroll_toggled)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setMaximumWidth(120)  # Set maximum width to match button
        self.speed_slider.valueChanged.connect(self.on_speed_changed)

        self.close_button = CustomButton("Close")
        self.close_button.clicked.connect(self.main_window.close)
        font = QFont()
        font.setFamilies([u"JetBrains Mono NL"])
        font.setBold(True)
        self.autoscroll_label = QLabel("Auto-Scroll Speed:")
        self.autoscroll_label.setStyleSheet("""color:#ffffff;
                                            font-size: 8pt;""")
        self.autoscroll_label.setFont(font)
        
        self.search_label = QLabel("Search:")
        self.search_box = QLineEdit()
        self.search_button = CustomButton("Search")
        self.search_button.clicked.connect(self.search_pdf)

        self.next_button = CustomButton(">")
        self.next_button.clicked.connect(self.next_occurrence)
        self.next_button.setFixedSize(60,40)

        self.prev_button = CustomButton("<")
        self.prev_button.clicked.connect(self.prev_occurrence)
        self.prev_button.setFixedSize(60,40)

        self.navigate_layout=QHBoxLayout()
        self.navigate_layout.addWidget(self.prev_button)
        self.navigate_layout.addWidget(self.next_button)

        self.search_results = []
        self.current_pos = -1
        self.container = QVBoxLayout()
        self.container.addWidget(self.meaning_button)
        self.container.addWidget(self.synonym_button)
        self.container.addWidget(self.speech_button)
        self.container.addWidget(self.auto_scroll_button)
        self.container.addWidget(self.autoscroll_label)
        self.container.addWidget(self.speed_slider)
        self.container.addWidget(self.search_label)
        self.container.addWidget(self.search_box)
        self.container.addWidget(self.search_button)
        self.container.addLayout(self.navigate_layout)
        self.container.addWidget(self.close_button)
        self.container.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.container)

    def on_meaning_button_clicked(self):
        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            definition = extra_functions.get_definition(selected_text)
            self.main_window.information.print_data(f"Meaning of {selected_text} : {definition}")

    def on_synonym_button_clicked(self):
        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            synonyms = extra_functions.get_synonyms(selected_text)
            if synonyms:
                self.main_window.information.print_data(f"Synonym of {selected_text} : {synonyms[0]}")

    def on_speech_button_clicked(self):
        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            extra_functions.get_word_pronunciation(selected_text)

    def on_auto_scroll_toggled(self, checked):
        if checked:
            self.main_window.start_auto_scroll()
        else:
            self.main_window.stop_auto_scroll()

    def on_speed_changed(self, value):
        self.main_window.set_auto_scroll_speed(value)

    def search_pdf(self):
        search_query = self.search_box.text()
        if search_query:
            # Set the cursor to the start of the document
            cursor = self.main_window.pdf_view.text_edit.textCursor()
            cursor.setPosition(0)
            self.main_window.pdf_view.text_edit.setTextCursor(cursor)
            
            # Clear previous search results
            self.search_results.clear()
            self.current_pos = -1
            
            # Search for all occurrences of the word
            while True:
                found_cursor = self.main_window.pdf_view.text_edit.document().find(search_query, cursor)
                if found_cursor.isNull():
                    break
                self.search_results.append(found_cursor)
                cursor = found_cursor

            if self.search_results:
                # Move the cursor to the first occurrence
                self.current_pos = 0
                self.main_window.pdf_view.text_edit.setTextCursor(self.search_results[self.current_pos])
                # Ensure the found word is visible
                self.main_window.pdf_view.text_edit.ensureCursorVisible()
            else:
                self.main_window.information.print_data("Search query not found.")

    def next_occurrence(self):
        if self.search_results:
            self.current_pos = (self.current_pos + 1) % len(self.search_results)
            self.main_window.pdf_view.text_edit.setTextCursor(self.search_results[self.current_pos])
            self.main_window.pdf_view.text_edit.ensureCursorVisible()

    def prev_occurrence(self):
        if self.search_results:
            self.current_pos = (self.current_pos - 1) % len(self.search_results)
            self.main_window.pdf_view.text_edit.setTextCursor(self.search_results[self.current_pos])
            self.main_window.pdf_view.text_edit.ensureCursorVisible()


class MainWindow(QWidget):
    def __init__(self, path):
        super().__init__()
        self.setWindowTitle("PySide6 PDF Viewer")
        self.pdf_view = PDFView(path)
        self.information = InfoLabel()
        self.button_holder = ButtonHolder(self)

        self.qlayout = QVBoxLayout()
        self.qlayout.addWidget(self.pdf_view.text_edit, 10)
        self.qlayout.addWidget(self.information.information, 1)
        self.hlayout = QHBoxLayout()
        self.hlayout.addLayout(self.qlayout, 10)
        self.hlayout.addWidget(self.button_holder, 1)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hlayout)

        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("""
            QWidget#pdf_view{
                background-color:#e0e0e0;
                color-black;
            }
            QWidget{
                background-color:#333333;
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
                background-color:  #353535;
                border: 1px solid black;             
                padding: 10px;
            }
            QPushButton:hover {
                background-color:#282828;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
        """)

        # Initialize QTimer for auto-scroll
        self.auto_scroll_timer = QTimer(self)
        self.auto_scroll_timer.timeout.connect(self.auto_scroll)
        self.auto_scroll_speed = 50  # Default auto-scroll speed
        self.is_auto_scrolling = False

    def start_auto_scroll(self):
        self.is_auto_scrolling = True
        self.auto_scroll_timer.start(1000 // self.auto_scroll_speed)

    def stop_auto_scroll(self):
        self.is_auto_scrolling = False
        self.auto_scroll_timer.stop()

    def set_auto_scroll_speed(self, speed):
        self.auto_scroll_speed = speed * 10
        if self.is_auto_scrolling:
            self.auto_scroll_timer.setInterval(1000 // speed)

    def auto_scroll(self):
        # Calculate the maximum scroll position
        max_scroll = self.pdf_view.text_edit.verticalScrollBar().maximum()
        # Increment scroll position
        current_scroll = self.pdf_view.text_edit.verticalScrollBar().value()
        new_scroll = current_scroll + 1
        if new_scroll > max_scroll:
            new_scroll = 0
        # Set new scroll position
        self.pdf_view.text_edit.verticalScrollBar().setValue(new_scroll)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("test.pdf")
    window.show()
    sys.exit(app.exec())
