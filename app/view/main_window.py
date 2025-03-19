from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout
from .portal_interface import PortalInterface
# from .course_interface import CourseInterface
from .setting_interface import SettingInterface
from qfluentwidgets import NavigationItemPosition, FluentWindow, setFont, SubtitleLabel, SplashScreen
from qfluentwidgets import FluentIcon as FIF
from ..common.icons import LocalIcon

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        self.show()
        self.portalInterface = PortalInterface(self)
        self.settingInterface = SettingInterface(self)
        # self.courseInterface = CourseInterface(self)
        self.initNavigation()
        self.splashScreen.finish()


    def initNavigation(self):
        # add sub interface
        self.addSubInterface(self.portalInterface, FIF.APPLICATION, self.tr('Portal'))
        # self.addSubInterface(self.courseInterface, FIF.APPLICATION, self.tr('course'))
        self.addSubInterface(self.settingInterface, FIF.SETTING,
                             self.tr('Settings'), NavigationItemPosition.BOTTOM)
        self.navigationInterface.setExpandWidth(280)

    def initWindow(self):
        self.resize(1000, 800)
        self.setWindowIcon(QIcon('app/images/icons/PKU_white.png'))
        self.setWindowTitle(self.tr('PKU-Course'))
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(160, 160))
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
