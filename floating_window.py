from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QFontDatabase, QFont
import constants


class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        font_id = QFontDatabase.addApplicationFont(constants.FONT)
        if font_id != -1:
            custom_font = QFont(QFontDatabase.applicationFontFamilies(
                font_id)[0], constants.FONT_SIZE)
        else:
            custom_font = QFont(constants.FONT_DEFAULT, constants.FONT_SIZE)

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        # Scroll area to hold text content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        text_widget = QWidget()
        text_layout = QVBoxLayout()

        # Label for displaying text
        self.text_label = QLabel()
        self.text_label.setFont(custom_font)
        self.text_label.setStyleSheet(f"""
            QLabel {{
                color: black;
                background-color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: {constants.FONT_SIZE}px;
            }}
        """)
        text_layout.addWidget(self.text_label)

        # Create the close button with "X" icon
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid white;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff4d4d;
                color: white;
            }
        """)
        self.close_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
        layout.addWidget(scroll_area)
        text_widget.setLayout(text_layout)
        scroll_area.setWidget(text_widget)

        self.setLayout(layout)
        self.setFixedSize(800, 500)

    def show_text(self, text):
        self.text_label.setText(text)
        self.adjust_size_and_position()
        self.show()

    def adjust_size_and_position(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.move(
            screen.width() - self.width() - 20,
            screen.height() - self.height() - 40
        )
