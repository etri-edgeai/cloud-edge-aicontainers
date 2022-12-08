import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

import requests

class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # repo list
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(30, 60, 111, 31))
        self.comboBox.addItem("aarch64")
        self.comboBox.addItem("x86")
        self.comboBox.addItem("x64")
        self.comboBox.addItem("x86_64")
        # texts
        label = QLabel('label1', self)
        label.setGeometry(QtCore.QRect(30, 30, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)

        label2 = QLabel('label2', self)
        label2.setGeometry(QtCore.QRect(170,30,91,21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        label2.setFont(font)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(170, 60, 121, 31))

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(320, 60, 131, 31))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        repo_list = QListWidget(self)
        repo_list.setGeometry(QtCore.QRect(20,160,231,251))
        search = requests.get('{url}/v2/_catalog'.format(url='http://172.26.64.1:5000'))
        nodes = eval(search.text)
        nodes = nodes['repositories']
        for n in nodes:
            repo_list.addItem(str(n))

        label3 = QLabel('label3', self)
        label3.setGeometry(QtCore.QRect(50,130,161,20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        label3.setFont(font)
        label3.setAlignment(QtCore.Qt.AlignCenter)

        label4 = QLabel('label4', self)
        label4.setGeometry(QtCore.QRect(290,159,141,31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        label4.setFont(font)
        label4.setAlignment(QtCore.Qt.AlignCenter)

        self.model_list = QListView(self)
        self.model_list.setGeometry(QtCore.QRect(270,200,191,211))

        self.setGeometry(300, 300, 488, 493)
        self.setWindowTitle('Edge Tool v0.1')
        repo_list.itemClicked.connect(self.show_models)
        self.buttonBox.clicked.connect(self.verify)
        self.show()
            
        
    def show_models(self, item):
        search2 = requests.get('{url}/v2/{repo}/tags/list'.format(url='http://172.26.64.1:5000', repo=str(item.text())))
        tags = eval(search2.text)
        tags = tags['tags']
        model = QStandardItemModel()
        for n in tags:
            model.appendRow(QStandardItem(n))
        self.model_list.setModel(model)

    def msgVerify(self, result):
        QMessageBox.information(self, "ALERT", result)

    def verify(self):
        reg_url = "http://172.26.64.1:5000"
        arch = self.comboBox.currentText()
        task = self.lineEdit.text()
        search = requests.get('{url}/v2/_catalog'.format(url=reg_url))
        print(search.text)
        model = "{arch}-model".format(arch=arch)

        if model in search.text:
            search2 = requests.get('{url}/v2/{model}/tags/list'.format(url=reg_url, model=model))
            print(search2.text)

            if task in search2.text:
                image_name = "{model}:{task}".format(model=model, task=task)
                result = """
We already have the model.

< download command >
docker pull {url}/{image_name}
                """.format(url=reg_url, image_name=image_name)
                self.msgVerify(result)

                
            else:
                result = 'We need to build a new one. Please activate distribution sequence.'
                QtWidgets.QMessageBox.information(self, "NOTICE", result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())