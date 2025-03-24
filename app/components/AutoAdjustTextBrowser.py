from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize, QByteArray, QUrl
from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QTextDocument, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from qfluentwidgets import TextBrowser
import requests


class AutoAdjustTextBrowser(TextBrowser):
    def __init__(self, session: requests.Session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setOpenExternalLinks(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.manager = QNetworkAccessManager()
        self.web_connection = True

    
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

    def loadResource(self, type, name):
        if self.web_connection:
            if type == QTextDocument.ResourceType.ImageResource.value:
                print(f'load image: {name.toString()}')
                url = name.toString()
                try:
                    response = self.session.get(url, stream=True)
                    response.raise_for_status()
                    image_data = response.content

                    pixmap = QPixmap()
                    pixmap.loadFromData(QByteArray(image_data))

                    self.document().addResource(
                        QTextDocument.ResourceType.ImageResource,
                        QUrl(url),
                        pixmap
                    )
                    return pixmap
                except requests.RequestException as e :
                    print(f'fail: {e}')
                    self.web_connection = False
                    return None

        return super().loadResource(type, name)
    
    def on_resource_loaded(self, reply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            pixmap = QPixmap()
            pixmap.loadFromData(reply.readAll())
            self.document().addResource(
                QTextDocument.ResourceType.ImageResource.value,
                reply.url(),
                pixmap
            )
            self.setDocument(self.document())
        else:
            print(reply.error().name)
        reply.deleteLater()