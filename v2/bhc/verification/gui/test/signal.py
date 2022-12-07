import sys

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
import requests


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.txt = ""
        self.lb = QLabel(str(self.txt))
        self.pb = QPushButton("get list")

        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("Custom Signal")
        form_lbx = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        self.setLayout(form_lbx)

        # 시그널 슬롯 연결
        self.pb.clicked.connect(self.count)

        form_lbx.addWidget(self.lb)
        form_lbx.addWidget(self.pb)

    @pyqtSlot()
    def count(self):
        search = requests.get('{url}/v2/_catalog'.format(url='http://172.26.64.1:5000'))
        self.txt = search.text
        self.lb.setText(str(self.txt))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())