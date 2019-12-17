import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel, QRubberBand, QPushButton
from PyQt5.QtCore import QPoint, QSize, Qt, QRect
from PyQt5.QtGui import QPixmap, QImage

class ImageView(QLabel):
    def __init__(self, parent=QWidget):
        super().__init__(parent)
        self.p1: QPoint
        self.p2: QPoint
        self.imgName: str
        self.imgType: str
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

    def setImage(self, pixmap: QPixmap):
        self.setPixmap(pixmap)
        self.resize(pixmap.size())
        self.rubberBand.hide()

    def setImageFromFile(self, imagePath: str):
        pixmap = QPixmap(imagePath)
        self.setImage(pixmap)
        self.imgName, self.imgType = imagePath.split('/')[-1].split('.')

    def cropSelection(self):
        if self.rubberBand.isHidden() is True:
            return
        rec = QRect(self.p1, self.p2)
        rec = self.rect().intersected(rec.normalized())
        image = self.pixmap().toImage()
        image = image.copy(rec)
        self.setImage(QPixmap.fromImage(image))

    def saveImage(self, path=str('.'), name=str(), t=str()):
        name = self.imgName if not name else name
        t = self.imgType if not t else t
        if not os.path.isdir(path):
            os.mkdir(path)
        self.pixmap().save(path + '/' + name + '.' + t, t)

    def mousePressEvent(self, event):
        if self.pixmap().isNull() or event.button() != Qt.LeftButton:
            return
        self.p1 = QPoint(event.pos())
        self.rubberBand.setGeometry(QRect(self.p1, QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if self.p1.isNull():
            return
        rec = QRect(self.p1, event.pos())
        self.rubberBand.setGeometry(rec.normalized())

    def mouseReleaseEvent(self, event):
        self.p2 = event.pos()
        QWidget.mouseReleaseEvent(self, event)
