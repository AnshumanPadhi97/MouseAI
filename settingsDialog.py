from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QSpinBox
import json


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(600, 400)
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.settings = self.load_settings()
        self.text_llm_model_input = QComboBox()
        self.text_llm_model_input.addItems(self.settings['MODEL_LIST'])
        form_layout.addRow("Text LLM Model:", self.text_llm_model_input)
        self.general_prompt_input = QLineEdit(
            self.settings['TEXT_LLM_GENERAL_PROMPT'])
        form_layout.addRow("General Prompt (Text):", self.general_prompt_input)
        self.code_prompt_input = QLineEdit(
            self.settings['CODE_LLM_GENERAL_PROMPT'])
        form_layout.addRow("General Prompt (Code):", self.code_prompt_input)
        self.font_size_input = QSpinBox()
        self.font_size_input.setValue(self.settings['FONT_SIZE'])
        self.font_size_input.setRange(10, 100)
        form_layout.addRow("Font Size:", self.font_size_input)
        self.button_size_input = QSpinBox()
        self.button_size_input.setValue(self.settings['BUTTON_SIZE'])
        self.button_size_input.setRange(10, 100)
        form_layout.addRow("Buttons Size:", self.button_size_input)
        self.window_width_input = QSpinBox()
        self.window_width_input.setRange(200, 1920)
        self.window_width_input.setValue(self.settings['WINDOW_WIDTH'])
        form_layout.addRow("Window Width:", self.window_width_input)
        self.window_height_input = QSpinBox()
        self.window_height_input.setRange(200, 1080)
        self.window_height_input.setValue(self.settings['WINDOW_HEIGHT'])
        form_layout.addRow("Window Height:", self.window_height_input)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception("Settings file not found")

    def save_settings(self):
        self.settings['TEXT_LLM_MODEL'] = self.text_llm_model_input.currentText()
        self.settings['TEXT_LLM_GENERAL_PROMPT'] = self.general_prompt_input.text()
        self.settings['CODE_LLM_GENERAL_PROMPT'] = self.code_prompt_input.text()
        self.settings['FONT_SIZE'] = self.font_size_input.value()
        self.settings['WINDOW_WIDTH'] = self.window_width_input.value()
        self.settings['WINDOW_HEIGHT'] = self.window_height_input.value()
        self.settings['BUTTON_SIZE'] = self.button_size_input.value()

        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)

        self.accept()
