from PyQt6 import QtCore
from qfluentwidgets import TransparentPushButton, TransparentToolButton, setCustomStyleSheet
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
        self.uri = None
        qss = """
        NavigationButton {
            padding: 0px !important;
            text-align: left;
        }
        """
        setCustomStyleSheet(self, qss, qss)
