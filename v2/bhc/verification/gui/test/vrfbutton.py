from PyQt5 import QtCore, QtGui, QtWidgets
import requests

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(486, 473)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(30, 60, 111, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(170, 30, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(170, 60, 121, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(320, 60, 131, 31))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.buttonBox.clicked.connect(self.verify)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.comboBox.setItemText(0, _translate("Dialog", "aarch64"))
        self.comboBox.setItemText(1, _translate("Dialog", "x86"))
        self.comboBox.setItemText(2, _translate("Dialog", "x86_64"))
        self.comboBox.setItemText(3, _translate("Dialog", "x64"))
        self.label.setText(_translate("Dialog", "MODEL"))
        self.label_2.setText(_translate("Dialog", "TASK"))


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
                
                print('we already have the model.')
                print("download command : 'docker pull {url}/{image_name}'".format(url=reg_url, image_name=image_name))

            else:

                print('activate distribution sequence.')



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())