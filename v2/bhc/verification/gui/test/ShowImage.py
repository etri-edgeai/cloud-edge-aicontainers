import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt



class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pixmap = QPixmap('data/test.jpeg')

        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_pred = QLabel('''
Top 5 result : 

dog 0.2107544243335724
cat 0.14806799590587616
horse 0.11213108897209167
bird 0.1107807531952858
deer 0.08659317344427109
        ''')
        lbl_pred.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.addWidget(lbl_pred)
        self.setLayout(vbox)

        self.setWindowTitle('Edge container tool')
        self.move(300, 300)
        self.show()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())