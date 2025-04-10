from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, pyqtSlot
from PyQt6.QtGui import QPixmap, QImage, QPainter, QIcon, QFont

from qfluentwidgets import CaptionLabel, FluentLabelBase, getFont, setCustomStyleSheet

class CourseMenuLabel(FluentLabelBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collapsed = False
        self.control_widget = None

    def getFont(self):
        return getFont(16, QFont.Weight.DemiBold)
    
    def connectControlWidget(self, control_widget):
        self.control_widget = control_widget
        self.animation = QPropertyAnimation(self.control_widget, b"maximumHeight")
        self.animation.setDuration(100)
        self.mousePressEvent = self.toggle_content_visibility

    @pyqtSlot()
    def toggle_content_visibility(self, event):
        if self.collapsed:
            new_height = self.control_widget.sizeHint().height()
            self.animation.setStartValue(0)
            self.animation.setEndValue(new_height)
        else:
            self.animation.setStartValue(self.control_widget.height())
            self.animation.setEndValue(0)
        
        self.animation.start()
        self.collapsed = not self.collapsed
    
class InfoLabel(CaptionLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        info_light_qss = """
        CaptionLabel {
        background-color: #06000000;
        border-radius: 10px;
        border: 1px solid #DDDDDD;
        padding: 1px 10px
        }"""
        info_dark_qss = """
        CaptionLabel {
        background-color: #11FFFFFF;
        border-radius: 10px;
        border: 1px solid #333333;
        padding: 1px 10px
        }"""
        setCustomStyleSheet(self, info_light_qss, info_dark_qss)
