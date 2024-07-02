from PyQt5.QtWidgets import QMessageBox,QInputDialog
from PyQt5.QtCore import *

# 设置定时器自动点击 OK
class AutoCloseMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super(AutoCloseMessageBox, self).__init__(*args, **kwargs)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.auto_click_ok) 
        self.timer.start(1000) # 定时器延迟时间，例如 1000 毫秒

    def auto_click_ok(self): # 模拟点击 OK 按钮
        self.accept()

class AutoInputDialog(QInputDialog):
    def __init__(self, parent=None):
        super(AutoInputDialog, self).__init__(parent)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.text = ""  # Initialize text as an empty string

    def set_auto_text(self, text, delay=800):
        self.text = text
        self.show()  # Ensure the dialog is displayed
        QTimer.singleShot(delay, lambda: self.setTextValue(str(self.text)))  # Fill text after delay
        QTimer.singleShot(2 * delay, self.accept)  # Accept after showing the text for a while