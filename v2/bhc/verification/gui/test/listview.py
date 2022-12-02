import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import requests


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        self.repo_list = QtWidgets.QListWidget(Dialog)
        self.repo_list.setGeometry(QtCore.QRect(20, 160, 231, 251))
        self.repo_list.setObjectName("repo_list")
        
        self.model_list = QtWidgets.QListView(Dialog)
        self.model_list.setGeometry(QtCore.QRect(270, 200, 191, 211))
        self.model_list.setObjectName("model_list")
        
        search = requests.get('{url}/v2/_catalog'.format(url='http://172.26.64.1:5000'))
        nodes = eval(search.text)
        nodes = nodes['repositories']
        for n in nodes:
            self.repo_list.addItem(str(n))
        
        self.repo_list.itemClicked.connect(self.show_models)
    

    def show_models(self, item):
        search2 = requests.get('{url}/v2/{repo}/tags/list'.format(url='http://172.26.64.1:5000', repo=str(item.text())))
        tags = eval(search2.text)
        tags = tags['tags']
        model = QStandardItemModel()
        for n in tags:
            model.appendRow(QStandardItem(n))
        self.model_list.setModel(model)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())