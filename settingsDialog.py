from PyQt5.QtWidgets import QMessageBox, QHBoxLayout, QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QSpinBox, QGroupBox
import constants
import json
import llm_manager


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(600, 400)
        layout = QVBoxLayout()
        self.ui_settings_group = self.create_section(
            title="UI Settings",
            form_layout=self.create_ui_settings_form()
        )
        self.ai_settings_group = self.create_section(
            title="AI Settings",
            form_layout=self.create_ai_settings_form()
        )
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.ai_settings_group)
        layout.addWidget(self.ui_settings_group)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def create_section(self, title, form_layout):
        group_box = QGroupBox(title)
        group_box.setLayout(form_layout)
        return group_box

    def create_ui_settings_form(self):
        form_layout = QFormLayout()
        self.settings = self.load_settings()
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
        return form_layout

    def create_ai_settings_form(self):
        form_layout = QFormLayout()
        self.text_llm_model_input = QComboBox()
        self.text_llm_model_input.clear()
        model_names = llm_manager.fetch_models_from_api()
        self.text_llm_model_input.addItems(model_names)
        saved_model = constants.TEXT_LLM_MODEL
        if saved_model and saved_model in model_names:
            self.text_llm_model_input.setCurrentText(saved_model)
        form_layout.addRow("Text AI Model:", self.text_llm_model_input)
        self.general_prompt_input = QLineEdit(
            self.settings['TEXT_LLM_GENERAL_PROMPT'])
        form_layout.addRow("General Prompt (Text):", self.general_prompt_input)
        self.code_prompt_input = QLineEdit(
            self.settings['CODE_LLM_GENERAL_PROMPT'])
        form_layout.addRow("General Prompt (Code):", self.code_prompt_input)
        self.open_model_dialog_button = QPushButton("Configure Models")
        self.open_model_dialog_button.clicked.connect(self.open_model_dialog)
        form_layout.addRow(self.open_model_dialog_button)
        return form_layout

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

    def open_model_dialog(self):
        model_dialog = ModelConfigurationDialog(self)
        model_dialog.exec_()


class ModelConfigurationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Models")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        self.model_combo = QComboBox(self)
        self.model_combo.addItems(llm_manager.fetch_models_from_api())
        h_layout.addWidget(self.model_combo)
        self.delete_button = QPushButton("Delete Model")
        self.delete_button.setFixedSize(100, 30)
        self.delete_button.clicked.connect(self.delete_model)
        h_layout.addWidget(self.delete_button)
        layout.addLayout(h_layout)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

    def delete_model(self):
        selected_model = self.model_combo.currentText()
        if selected_model:
            try:
                llm_manager.delete_ollama_model(selected_model)
                QMessageBox.information(self, "Success", f"Model {
                                        selected_model} deleted successfully.")
                self.model_combo.clear()
                self.model_combo.addItems(llm_manager.fetch_models_from_api())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting model {
                                     selected_model}: {e}")
        else:
            QMessageBox.warning(
                self, "Warning", "No model selected for deletion.")
