import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

import requests

class BuildWindow(QDialog,QWidget):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300)

        btn1 = QPushButton("upload files", self)
        btn1.setGeometry(390, 50, 100, 30)
        btn1.clicked.connect(self.btn_fun_FileLoad)
        
        btn2 = QPushButton('copy files', self)
        btn2.setGeometry(390, 100, 100, 30)
        btn2.clicked.connect(self.copy_files)

        self.fileview = QListView(self)
        self.fileview.setGeometry(10, 50, 370, 180)

        btn3 = QPushButton('start build', self)
        btn3.setGeometry(200, 250, 100, 30)
        btn3.clicked.connect(self.build)

        btn4 = QPushButton('Cancel', self)
        btn4.setGeometry(330, 250, 100, 30)
        btn4.clicked.connect(self.home)


    def btn_fun_FileLoad(self):
        
        global Dockerfile_path, zipModel_path

        fname = QFileDialog.getOpenFileNames(self)
        model = QStandardItemModel()
        for f in fname[0]:
            if 'Dockerfile' in f:
                Dockerfile_path = f
                model.appendRow(QStandardItem(Dockerfile_path))
            else:
                zipModel_path = f
                model.appendRow(QStandardItem(zipModel_path))
        self.fileview.setModel(model)


    def copy_files(self):
        os.system('ansible-playbook copy.yaml -e "Dockerfile_path={Dockerfile_path} zipModel_path={zipModel_path}"'.format(Dockerfile_path=Dockerfile_path, zipModel_path=zipModel_path))

    def build(self):
        print('check network session...')
        print()
        os.system('ansible builders -m ping')
        os.system('ansible builders -m command -a "ls -alF"')
        print()
        print()
        print("start image build & distribution...")
        print()
        os.system('ansible-playbook autorun.yaml -e "tag={tag} registry={reg_url}"'.foramt(tag=tag, reg_url=reg_url))

    def home(self):
        self.close()

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
        label = QLabel('ARCH', self)
        label.setGeometry(QtCore.QRect(30, 30, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)

        label2 = QLabel('TAG', self)
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

        label3 = QLabel('REPOSITORIES', self)
        label3.setGeometry(QtCore.QRect(50,130,161,20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        label3.setFont(font)
        label3.setAlignment(QtCore.Qt.AlignCenter)

        label4 = QLabel('MODEL_LIST', self)
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

        global tag

        search2 = requests.get('{url}/v2/{repo}/tags/list'.format(url='http://172.26.64.1:5000', repo=str(item.text())))
        tag = eval(search2.text)
        tag = tag['tags']
        model = QStandardItemModel()
        for n in tag:
            model.appendRow(QStandardItem(n))
        self.model_list.setModel(model)

    def verify(self):

        global reg_url

        reg_url = "http://172.26.64.1:5000"
        arch = self.comboBox.currentText()
        task = self.lineEdit.text()
        search = requests.get('{url}/v2/_catalog'.format(url=reg_url))
        model = "{arch}-model".format(arch=arch)

        if model in search.text:
            search2 = requests.get('{url}/v2/{model}/tags/list'.format(url=reg_url, model=model))

            if task in search2.text:
                image_name = "{model}:{task}".format(model=model, task=task)
                result = """
We already have the model.

< download command >
docker pull {url}/{image_name}
                """.format(url=reg_url, image_name=image_name)
                QtWidgets.QMessageBox.information(self, "ALERT", result)

                
            else:
                result = 'We need to build a new one. Please activate distribution sequence.'
                reply = QtWidgets.QMessageBox.question(self, "ALERT", result, QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.show_BuildWindow()
                    

    def show_BuildWindow(self):
        self.hide()
        self.second = BuildWindow()
        self.second.exec()
        self.show()
                    





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())