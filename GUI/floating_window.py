from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QGuiApplication, QFontDatabase, QFont, QIcon
import Settings.constants as constants
import LLM.llm_manager as llm_manager
import GUI.settingsDialog as settingsDialog


class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.file_paths = []
        self.loading_label = None
        self.init_ui()

    def init_ui(self):
        self.setAcceptDrops(True)
        font_id = QFontDatabase.addApplicationFont(
            "Asests\\Delius-Regular.ttf")
        if font_id != -1:
            custom_font = QFont(QFontDatabase.applicationFontFamilies(
                font_id)[0], constants.FONT_SIZE)
        else:
            custom_font = QFont("Arial", constants.FONT_SIZE)
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
        self.close_button.setFixedSize(
            constants.BUTTON_SIZE, constants.BUTTON_SIZE)
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
        self.chat_button.setIcon(QIcon("Asests\\comment.png"))
        self.chat_button.setFixedSize(
            constants.BUTTON_SIZE, constants.BUTTON_SIZE)
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
        self.minimize_button.setIcon(QIcon("Asests\\minimize.png"))
        self.minimize_button.setFixedSize(
            constants.BUTTON_SIZE, constants.BUTTON_SIZE)
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
        self.drag_button.setIcon(QIcon("Asests\\dir.png"))
        self.drag_button.setFixedSize(
            constants.BUTTON_SIZE, constants.BUTTON_SIZE)
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
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("Asests\\settings.png"))
        self.settings_button.setFixedSize(
            constants.BUTTON_SIZE, constants.BUTTON_SIZE)
        self.settings_button.setStyleSheet("""
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
        self.settings_button.clicked.connect(self.open_settings_dialog)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.chat_button)
        button_layout.addStretch()
        button_layout.addWidget(self.drag_button)
        button_layout.addWidget(self.minimize_button)
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.scroll_area)
        self.chat_input_field = QTextEdit()
        self.chat_input_field.setFont(custom_font)
        self.chat_input_field.setFixedHeight(constants.BUTTON_SIZE * 2)
        self.chat_input_field.setPlaceholderText("Type your message...")
        self.chat_input_field.setStyleSheet(
            f"QTextEdit {{ font-size: {constants.FONT_SIZE}px; padding: 5px; }}")
        self.chat_input_field.setFocus()
        self.send_button = QPushButton()
        self.send_button.setFixedSize(
            constants.BUTTON_SIZE, constants.BUTTON_SIZE)
        self.send_button.setIcon(QIcon("Asests\\send.png"))
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
        self.clear_button.setFixedSize(
            constants.BUTTON_SIZE, constants.BUTTON_SIZE)
        self.clear_button.setIcon(QIcon("Asests\\broom.png"))
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
        self.setFixedSize(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)

    def open_settings_dialog(self):
        settings_dialog = settingsDialog.SettingsDialog(self)
        settings_dialog.exec_()

    def create_loading_label(self):
        self.loading_label = QLabel("Processing...", self)
        self.loading_label.setFont(self.customFont)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet(f"""
            QLabel {{
                font-size: {constants.FONT_SIZE}px;
                color: white;
                background-color: rgba(0, 0, 0, 128);
                border-radius: 10px;
                padding: 10px;
            }}
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
        if not is_visible:
            self.chat_input_field.setFocus()

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
        self.file_paths = []
        llm_manager.clear_rag()

    def show_chat(self):
        self.handle_message(None)

    def add_message_to_chat(self, message, sender):
        label = QLabel(message)
        label.setWordWrap(True)
        label.setFont(self.customFont)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setStyleSheet(f"""
            QLabel {{
                background-color: lightgray;
                border-radius: 10px;
                padding: 8px;
                font-size: {constants.FONT_SIZE}px;
            }}
        """)

        if sender == 'user':
            label.setAlignment(Qt.AlignRight)
            label.setStyleSheet(f"""
                QLabel {{
                    background-color: #e6f7ff;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: {constants.FONT_SIZE}px;
                }}
            """)
        elif sender == 'assistant':
            label.setAlignment(Qt.AlignLeft)
            label.setStyleSheet(f"""
                QLabel {{
                    background-color: #cce5ff;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: {constants.FONT_SIZE}px;
                }}
            """)

        self.chat_area.addWidget(label)
        self.show()

    def add_system_message(self, message):
        system_label = QLabel(message)
        system_label.setWordWrap(True)
        system_label.setFont(self.customFont)
        system_label.setAlignment(Qt.AlignLeft)
        system_label.setStyleSheet(f"""
            QLabel {{
                font-size: {constants.FONT_SIZE - 2}px;
                font-style: italic;
                color: gray;
                background-color: transparent;
                padding: 10px;
            }}
        """)
        self.chat_area.addWidget(system_label)
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_urls = event.mimeData().urls()
        if file_urls:
            self.file_paths = [url.toLocalFile() for url in file_urls]
            self.handle_files()

    def show_text(self, text):
        self.handle_message(
            constants.TEXT_LLM_GENERAL_PROMPT + " " + text + "?")

    def send_message(self):
        user_message = self.chat_input_field.toPlainText().strip()
        if user_message:
            self.handle_message(user_message)
            self.chat_input_field.clear()
        else:
            self.chat_input_field.setText(
                "Message is empty. Please type something.")

    # Handle messages/files in these function for LLM interaction

    def handle_message(self, text):
        self.adjust_size_and_position()

        if text is not None:
            text = text.strip()

        if text:
            if self.loading_label is None:
                self.create_loading_label()
            self.loading_label.setVisible(True)

            self.add_message_to_chat(text, 'user')
            self.messages.append({
                'role': 'user',
                'content': text
            })

            QTimer.singleShot(100, lambda: self.process_llm(text))
        else:
            self.show()

    def process_llm(self, current_text):
        response = llm_manager.llm_response(
            self.file_paths, self.messages, current_text)

        if self.loading_label:
            self.loading_label.setVisible(False)

        self.messages.append({
            'role': 'assistant',
            'content': response
        })
        self.add_message_to_chat(response, 'assistant')

    def handle_files(self):
        self.process_llm_files()

    def process_llm_files(self):
        response = llm_manager.process_rag_files(self.file_paths)
        message = ''
        if response == True:
            message = "Documents are ready for Q&A"
        else:
            message = "Unable to process documents/No documents found to process"
        self.add_system_message(message)
