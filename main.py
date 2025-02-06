import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread
from Core.text_monitor import TextMonitor


def main():
    app = QApplication(sys.argv)
    monitor = TextMonitor()
    monitor_thread = QThread()
    monitor.moveToThread(monitor_thread)
    monitor_thread.started.connect(monitor.start_monitoring)
    monitor_thread.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
