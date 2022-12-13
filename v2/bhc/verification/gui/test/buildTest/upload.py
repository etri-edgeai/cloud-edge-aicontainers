import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyWindow(QMainWindow):
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


    def btn_fun_FileLoad(self):
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
        pass


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()