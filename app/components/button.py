from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QPainter, QIcon

from qfluentwidgets import TransparentPushButton, TransparentToolButton
from ..common.icons import LocalIcon

class PKULogoButton(TransparentToolButton):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setIcon(LocalIcon.PKUFULL)
        self.setIconSize(QtCore.QSize(107, 30))
        self.setFixedSize(QtCore.QSize(120, 30))

class NavigationButton(TransparentPushButton):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.connect_url = None
        current_style = self.styleSheet()
        additional_styles = """
        NavigationButton {
            padding: 0px !important;
            text-align: left;
        }
        """
        self.setStyleSheet(current_style + ' ' + additional_styles)
