from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize, QByteArray, QUrl
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QTextDocument, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from qfluentwidgets import TextBrowser
import requests


class AutoAdjustTextBrowser(TextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOpenExternalLinks(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    
    def sizeHint(self):
        self.document().setTextWidth(self.viewport().width())
        doc_height = self.document().size().height()
        margin = self.document().documentMargin() * 2
        frame = self.frameWidth() * 2
        total_height = doc_height + margin + frame
        return QSize(super().sizeHint().width(), int(total_height))
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGeometry()
        self.setFixedHeight(self.sizeHint().height())