import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyWindow(QWidget):

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
    

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()