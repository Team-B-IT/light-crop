import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QScrollArea
from PyQt5.QtWidgets import QLabel, QPushButton, QButtonGroup, QListView, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QPainter
from fileListView import FileListView
from imageView import ImageView

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initEvent()
        self.setMinimumSize(720, 480)
        self.show()

    def initUI(self):
        self.image = ImageView(self)

        self.viewer = QScrollArea(self)
        self.viewer.setWidget(self.image)

        #self.clearBtn = QPushButton("Clear", self)
        self.openBtn = QPushButton("Open file(s) (O)", self)
        self.cropBtn = QPushButton("Crop (C)", self)
        self.saveBtn = QPushButton("Save (S)", self)

        self.listView = FileListView(self)

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.viewer, 0, 0, 10, 8)
        mainLayout.addWidget(self.openBtn, 0, 9)
        mainLayout.addWidget(self.saveBtn, 0, 10)
        mainLayout.addWidget(self.cropBtn, 1, 9)
        #mainLayout.addWidget(buttonLayout)
        mainLayout.addWidget(self.listView, 2, 9, 8, 2)
        #self.setLayout(mainLayout)

    def initEvent(self):
        self.cropBtn.clicked.connect(self.cropBtnClicked)
        self.openBtn.clicked.connect(self.openBtnClicked)
        self.saveBtn.clicked.connect(self.saveBtnClicked)
        self.listView.clicked.connect(self.listSelected)

    def openBtnClicked(self):
        filters = "Images (*.jpg *.jpeg *.jpe *.png *.jp2 *.bmp)"
        ds = QFileDialog.getOpenFileNames(self, "Open image file(s)", "./", filters)
        self.listView.addItems(ds[0])

    def cropBtnClicked(self):
        self.image.cropSelection()

    def saveBtnClicked(self):
        self.image.saveImage("./cropped")

    def listSelected(self):
        path = self.listView.getSelectedItem()
        self.image.setImageFromFile(path)

    def keyPressEvent(self, event):
        switcher = {
            Qt.Key_C: self.cropBtnClicked,
            Qt.Key_S: self.saveBtnClicked,
            Qt.Key_O: self.openBtnClicked
        }
        func = switcher.get(event.key(), False)
        if func is not False:
            func()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()
