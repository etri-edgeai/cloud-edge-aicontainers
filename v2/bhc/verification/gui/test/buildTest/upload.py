import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300)

        btn1 = QPushButton("load",self)
        btn1.clicked.connect(self.btn_fun_FileLoad)
        btn2 = QPushButton('copy', self)
        btn2.clicked.connect(self.copy_files)

    def btn_fun_FileLoad(self):
        fname = QFileDialog.getOpenFileNames(self)
        for f in fname[0]:
            if 'Dockerfile' in f:
                Dockerfile_path = f
            else:
                zipModel_path = f
        print(Dockerfile_path)
        print(zipModel_path)

    def copy_files(self):
        pass

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()