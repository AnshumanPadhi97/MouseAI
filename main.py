import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QThread
from text_monitor import TextMonitor
import llm_manager
import Utils


def main():
    app = QApplication(sys.argv)

    if not llm_manager.is_ollama_running():
        Utils.show_ok_popup(QMessageBox.Critical, "Warning",
                            "Ollama is not running. Please start Ollama and try again.")
        sys.exit(1)

    monitor = TextMonitor()
    monitor_thread = QThread()
    monitor.moveToThread(monitor_thread)
    monitor_thread.started.connect(monitor.start_monitoring)
    monitor_thread.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
