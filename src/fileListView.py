from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QListView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex

class FileListView(QListView):
    def __init__(self, parent=QWidget):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def addItems(self, items):
        for item in items:
            self.addItem(item)
        self.sortItem()

    def addItem(self, item):
        if self.model.findItems(item):
            return
        self.model.appendRow(QStandardItem(item))

    def removeItem(self, item):
        row = self.model.indexFromItem(QStandardItem(item))
        self.model.removeRow(row)

    def getSelectedItem(self):
        for item in self.selectionModel().selectedIndexes():
            return item.data()

    def sortItem(self):
        self.model.sort(0)

    def clear(self):
        self.model.clear()
