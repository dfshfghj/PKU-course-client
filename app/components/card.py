from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from qfluentwidgets import CardWidget, BodyLabel, IconWidget, SubtitleLabel, TextBrowser, FluentIcon, CaptionLabel, HorizontalSeparator, SimpleCardWidget, isDarkTheme
from ..components.label import InfoLabel

class AnnouncementCard(CardWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.announcementTitleLabel = SubtitleLabel("testAnnouncementTitle", self)
        self.announcementTitleLabel.setObjectName("announcementTitleLabel")
        self.verticalLayout.addWidget(self.announcementTitleLabel)
        self.announcementInfo = QtWidgets.QHBoxLayout()
        self.announcementInfo.setObjectName("announcementInfo")
        self.info_1 = InfoLabel("testInfo1", self)
        self.info_1.setObjectName("info_1")
        self.announcementInfo.addWidget(self.info_1)
        self.info_2 = InfoLabel("testInfo2", self)
        self.info_2.setObjectName("info_2")
        self.announcementInfo.addWidget(self.info_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.announcementInfo.addItem(spacerItem)
        self.verticalLayout.addLayout(self.announcementInfo)
        self.announcementDetails = QtWidgets.QHBoxLayout()
        self.announcementDetails.setObjectName("announcementDetails")
        self.icon = IconWidget(FluentIcon.STOP_WATCH, self)
        self.icon.setFixedSize(16, 16)
        self.icon.setObjectName("icon")
        self.announcementDetails.addWidget(self.icon)
        self.detailsLabel = BodyLabel("testDetails", self)
        self.detailsLabel.setObjectName("detailsLabel")
        self.announcementDetails.addWidget(self.detailsLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.announcementDetails.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.announcementDetails)
        #self.textBrowser = AutoAdjustTextBrowser(parent=self)
        #self.textBrowser.setObjectName("textBrowser")
        self.bodyLabel = BodyLabel(self)
        self.bodyLabel.setObjectName("bodyLabel")
        self.bodyLabel.setWordWrap(True)
        self.verticalLayout.addWidget(self.bodyLabel)

    def addHtml(self, html):
        self.bodyLabel.setText(html)

class DocumentCard(CardWidget):
    def __init__(self, icon, detail: bool, parent):
        super().__init__(parent=parent)
        self.href = ''
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon = IconWidget(icon, self)
        self.icon.setObjectName('icon')
        self.icon.setFixedSize(24, 24)
        self.horizontalLayout.addWidget(self.icon)
        font = QFont()
        font.setBold(True)
        self.title = BodyLabel(self)
        self.title.setFont(font)
        self.title.setWordWrap(True)
        self.title.setObjectName('title')
        self.horizontalLayout.addWidget(self.title)
        self.horizontalSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.addLayout(self.horizontalLayout)
        if detail:
            self.horizontalSeparator = HorizontalSeparator(self)
            self.horizontalSeparator.setObjectName('horizontalSeparator')
            self.verticalLayout.addWidget(self.horizontalSeparator)
            self.details = CaptionLabel(self)
            #self.details.setTextFormat(Qt.TextFormat.MarkdownText)
            self.details.setTextFormat(Qt.TextFormat.RichText)
            self.details.setObjectName("details")
            self.details.setWordWrap(True)
            self.verticalLayout.addWidget(self.details)

class LoginPanelCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _normalBackgroundColor(self):
        if isDarkTheme:
            return QColor(255, 255, 255, 50)
        else:
            return QColor(255, 255, 255 ,170) 
            