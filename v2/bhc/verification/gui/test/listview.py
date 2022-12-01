import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import requests


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.Registry_list = QtWidgets.QListView(Dialog)
        self.Registry_list.setGeometry(QtCore.QRect(20, 160, 231, 251))
        self.Registry_list.setObjectName("Registry_list")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(270, 200, 191, 211))
        self.listWidget.setObjectName("listWidget")
        
        search = requests.get('{url}/v2/_catalog'.format(url='http://172.26.64.1:5000'))
        nodes = eval(search.text)
        nodes = nodes['repositories']
        model = QStandardItemModel()
        for n in nodes:
            model.appendRow(QStandardItem(n))
        self.Registry_list.setModel(model)





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())