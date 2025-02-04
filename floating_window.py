from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QGuiApplication, QFontDatabase, QFont, QIcon, QMovie
import constants
import llm_manager
from PyQt5.QtWidgets import QDialog


class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.messages = []
        self.loading_label = None

    def init_ui(self):
        font_id = QFontDatabase.addApplicationFont(constants.FONT)
        if font_id != -1:
            custom_font = QFont(QFontDatabase.applicationFontFamilies(
                font_id)[0], constants.FONT_SIZE)
        else:
            custom_font = QFont(constants.FONT_DEFAULT, constants.FONT_SIZE)
        self.customFont = custom_font
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        text_widget = QWidget()
        self.chat_area = QVBoxLayout()
        text_widget.setLayout(self.chat_area)
        self.scroll_area.setWidget(text_widget)
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
        self.chat_button = QPushButton()
        self.chat_button.setIcon(QIcon(constants.CHAT_ICON))
        self.chat_button.setFixedSize(30, 30)
        self.chat_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid white;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4d94ff;
                color: white;
            }
        """)
        self.chat_button.clicked.connect(self.toggle_chat_input)
        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(QIcon(constants.MINIMIZE_ICON))
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid white;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4d94ff;
                color: white;
            }
        """)
        self.minimize_button.clicked.connect(self.toggle_ui)
        self.drag_button = QPushButton()
        self.drag_button.setIcon(QIcon(constants.DRAG_ICON))
        self.drag_button.setFixedSize(30, 30)
        self.drag_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid white;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
        """)
        self.is_dragging = False
        self.drag_position = QPoint()
        self.drag_button.setMouseTracking(True)
        self.drag_button.mousePressEvent = self.start_drag
        self.drag_button.mouseMoveEvent = self.drag_move
        self.drag_button.mouseReleaseEvent = self.end_drag
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.chat_button)
        button_layout.addStretch()
        button_layout.addWidget(self.drag_button)
        button_layout.addWidget(self.minimize_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.scroll_area)
        self.chat_input_field = QLineEdit()
        self.chat_input_field.setFont(custom_font)
        self.chat_input_field.setPlaceholderText("Type your message...")
        self.chat_input_field.setStyleSheet(
            "QLineEdit { font-size: 16px; padding: 5px; }")
        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon(constants.SEND_ICON))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid white;
                color: white;
                font-size: 16px;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4d94ff;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        self.clear_button = QPushButton()
        self.clear_button.setIcon(QIcon(constants.CLEAR_ICON))
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid white;
                color: white;
                font-size: 16px;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4d94ff;
            }
        """)
        self.clear_button.clicked.connect(self.clear_messages)
        self.chat_layout = QHBoxLayout()
        self.chat_layout.addWidget(self.chat_input_field)
        self.chat_layout.addWidget(self.send_button)
        self.chat_layout.addWidget(self.clear_button)
        layout.addLayout(self.chat_layout)
        self.setLayout(layout)
        self.setFixedSize(800, 500)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_input_field.setVisible(False)
        self.send_button.setVisible(False)
        self.clear_button.setVisible(False)

    def create_loading_label(self):
        self.loading_label = QLabel("Processing...", self)
        self.loading_label.setFont(self.customFont)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: white;
                background-color: rgba(0, 0, 0, 128);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.loading_label.setFixedSize(200, 100)
        self.loading_label.move(self.width() // 2 - 100,
                                self.height() // 2 - 50)
        self.loading_label.setVisible(False)

    def start_drag(self, event):
        self.is_dragging = True
        self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def drag_move(self, event):
        if self.is_dragging:
            self.move(event.globalPos() - self.drag_position)

    def end_drag(self, event):
        self.is_dragging = False

    def toggle_chat_input(self):
        is_visible = self.chat_input_field.isVisible()
        self.chat_input_field.setVisible(not is_visible)
        self.send_button.setVisible(not is_visible)
        self.clear_button.setVisible(not is_visible)

    def toggle_ui(self):
        self.close_button.setVisible(True)
        self.minimize_button.setVisible(True)
        self.drag_button.setVisible(True)
        self.chat_input_field.setVisible(False)
        self.send_button.setVisible(False)
        self.clear_button.setVisible(False)
        is_visible = self.chat_button.isVisible()
        self.scroll_area.setVisible(not is_visible)
        self.chat_button.setVisible(not is_visible)
        if not is_visible:
            self.adjust_size_and_position()

    def adjust_size_and_position(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.move(
            screen.width() - self.width() - 20,
            screen.height() - self.height() - 40
        )

    def clear_messages(self):
        for i in range(self.chat_area.count()):
            widget = self.chat_area.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.messages = []

    def add_message_to_chat(self, message, sender):
        label = QLabel(message)
        label.setWordWrap(True)
        label.setFont(self.customFont)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setStyleSheet("""
            QLabel {
                background-color: lightgray;
                border-radius: 10px;
                padding: 8px;
                font-size: 16px;
            }
        """)
        if sender == 'user':
            label.setAlignment(Qt.AlignRight)
            label.setStyleSheet("""
                QLabel {
                    background-color: #e6f7ff;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 16px;
                }
            """)
        elif sender == 'assistant':
            label.setAlignment(Qt.AlignLeft)
            label.setStyleSheet("""
                QLabel {
                    background-color: #cce5ff;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 16px;
                }
            """)
        self.chat_area.addWidget(label)
        self.show()

    def show_text(self, text):
        self.handle_message(text, 'clipboard')

    def send_message(self):
        user_message = self.chat_input_field.text().strip()
        if user_message:
            self.handle_message(user_message, 'chat')
            self.chat_input_field.clear()
        else:
            self.chat_input_field.setText(
                "Message is empty. Please type something.")

    def handle_message(self, text, type):
        if self.loading_label is None:
            self.create_loading_label()
        self.loading_label.setVisible(True)

        self.adjust_size_and_position()
        text = text.strip()
        if text:
            if type == "clipboard":
                text = constants.TEXT_LLM_GENERAL_PROMPT + text + "?"

            self.add_message_to_chat(text, 'user')
            self.messages.append({
                'role': 'user',
                'content': text
            })
            QTimer.singleShot(100, lambda: self.process_text_llm())
        else:
            self.show()

    def process_text_llm(self):
        llm_response = llm_manager.llm_chat_text_response(self.messages)

        if self.loading_label:
            self.loading_label.setVisible(False)

        self.messages.append({
            'role': 'assistant',
            'content': llm_response
        })
        self.add_message_to_chat(llm_response, 'assistant')
