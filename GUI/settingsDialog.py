from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QSpinBox, QGroupBox
import json
import LLM.llm_manager as llm_manager
import Settings.constants as constants


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

        self.ai_provider_input = QComboBox()
        self.ai_provider_input.addItem("OLLAMA")
        self.ai_provider_input.addItem("AnotherProvider")

        self.ai_provider_input.setCurrentText(constants.AI_PROVIDER)
        self.ai_provider_input.currentTextChanged.connect(
            self.update_model_list)
        form_layout.addRow("AI Provider:", self.ai_provider_input)

        self.general_prompt_input = QLineEdit(
            self.settings['TEXT_LLM_GENERAL_PROMPT'])
        form_layout.addRow("General Prompt:", self.general_prompt_input)

        self.model_selection_input = QComboBox()
        self.update_model_list()
        form_layout.addRow("Select Model:", self.model_selection_input)

        self.delete_model_button = QPushButton("Delete Selected Model")
        self.delete_model_button.clicked.connect(self.delete_model)
        form_layout.addRow(self.delete_model_button)

        return form_layout

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception("Settings file not found")

    def save_settings(self):
        self.settings['TEXT_LLM_GENERAL_PROMPT'] = self.general_prompt_input.text()
        self.settings['TEXT_LLM_MODEL'] = self.model_selection_input.currentText()
        self.settings['FONT_SIZE'] = self.font_size_input.value()
        self.settings['WINDOW_WIDTH'] = self.window_width_input.value()
        self.settings['WINDOW_HEIGHT'] = self.window_height_input.value()
        self.settings['BUTTON_SIZE'] = self.button_size_input.value()
        self.settings['AI_PROVIDER'] = self.ai_provider_input.currentText()
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
        self.accept()

    def update_model_list(self):
        model_names = llm_manager.get_models()
        self.model_selection_input.clear()
        self.model_selection_input.addItems(model_names)
        if model_names:
            self.model_selection_input.setCurrentIndex(0)

    def delete_model(self):
        selected_model = self.model_selection_input.currentText()
        if selected_model:
            try:
                llm_manager.delete_model(selected_model)
                QMessageBox.information(self, "Success", f"Model {
                                        selected_model} deleted successfully.")
                self.update_model_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting model {
                                     selected_model}: {e}")
        else:
            QMessageBox.warning(
                self, "Warning", "No model selected for deletion.")
