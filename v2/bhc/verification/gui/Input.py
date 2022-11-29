import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl1 = QLabel('Enter your CPU Architecture.', self)
        lbl1.move(10, 10)
        font1 = lbl1.font()
        lbl1.setFont(font1)

        lbl2 = QLabel('Enter your Model Task.', self)
        lbl2.move(10, 70)
        font2 = lbl2.font()
        lbl2.setFont(font2)

        layout = QVBoxLayout()
        layout.addWidget(lbl1)
        layout.addWidget(lbl2)

        te = QLineEdit(self)
        te.move(10, 30)
        te.textChanged[str].connect(self.onChanged)
        
        te2 = QLineEdit(self)
        te2.move(10, 90)
        te2.textChanged[str].connect(self.onChanged)


        self.setWindowTitle('Edge container tool')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def onChanged(self, text):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())