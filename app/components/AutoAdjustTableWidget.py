from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize, QByteArray, QUrl
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QTextDocument, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from qfluentwidgets import TableWidget
import requests


class AutoAdjustTableWidget(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def sizeHint(self):
        height = sum(self.rowHeight(i) for i in range(self.rowCount())) + \
            self.horizontalHeader().height() + self.frameWidth() * 2
        return QSize(super().sizeHint().width(), height)
    
