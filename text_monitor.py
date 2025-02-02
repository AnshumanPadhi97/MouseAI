from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication
import keyboard
from clipboard_manager import ClipboardManager
from floating_window import FloatingWindow


class TextMonitor(QObject):
    text_selected = pyqtSignal(str)  # Signal to emit when text is selected

    def __init__(self):
        super().__init__()
        self.clipboard_manager = ClipboardManager()
        self.window = FloatingWindow()
        # Connect the signal to the window's show_text method
        self.text_selected.connect(self.window.show_text)

    def start_monitoring(self):
        keyboard.add_hotkey('ctrl+space', self.on_hotkey)
        keyboard.hook(self.on_key_event)

    def on_hotkey(self):
        selected_text = self.clipboard_manager.get_selected_text()
        if selected_text.strip():
            # Emit the signal instead of directly calling show_text
            self.text_selected.emit(selected_text)

    def on_key_event(self, event):
        if event.name == 'q' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
            self.exit_application()

    def exit_application(self):
        # Perform any necessary cleanup here, like stopping threads or closing resources
        print("Cleaning up and exiting...")
        keyboard.unhook_all()  # Unhook all keyboard listeners to prevent further events
        QCoreApplication.quit()  # Properly quit the PyQt application
