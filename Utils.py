from PyQt5.QtWidgets import QMessageBox


def show_ok_popup(icon, title, message):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
