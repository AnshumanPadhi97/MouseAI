from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication
import keyboard
from clipboard_manager import ClipboardManager
from floating_window import FloatingWindow


class TextMonitor(QObject):
    text_selected = pyqtSignal(str)
    show_chat = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.clipboard_manager = ClipboardManager()
        self.window = FloatingWindow()
        self.text_selected.connect(self.window.show_text)
        self.show_chat.connect(self.window.show_chat)

    def on_key_event(self, event):
        if event.name == 'q' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
            self.exit_application()

    def exit_application(self):
        print("Cleaning up and exiting...")
        keyboard.unhook_all()
        QCoreApplication.quit()

    def start_monitoring(self):
        keyboard.add_hotkey('ctrl+space', self.on_search)
        keyboard.add_hotkey('ctrl+shift+c', self.on_chat)
        keyboard.hook(self.on_key_event)

    def on_search(self):
        selected_text = self.clipboard_manager.get_selected_text()
        self.text_selected.emit(selected_text)

    def on_chat(self):
        self.show_chat.emit()
