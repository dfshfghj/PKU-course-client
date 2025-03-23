from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout
from .portal_interface import PortalInterface
from .login_interface import LoginInterface
# from .course_interface import CourseInterface
from .setting_interface import SettingInterface
from qfluentwidgets import NavigationItemPosition, FluentWindow, setFont, SubtitleLabel, SplashScreen
from qfluentwidgets import FluentIcon as FIF
from ..common.icons import LocalIcon
from ..common.course_requests import Client
import json
from .. import resources_rc

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        self.show()
        if self.login_test():
            self.portalInterface = PortalInterface(self.client, self)
        else:
            self.portalInterface = LoginInterface(self.client, self)
        self.settingInterface = SettingInterface(self)
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
        self.setWindowIcon(QIcon(':/images/icons/PKU_white.png'))
        self.setWindowTitle(self.tr('PKU-Course'))
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(160, 160))
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def login_test(self):
        self.client = Client()
        with open('data/login.json', 'r', encoding='utf-8') as file:
            login = json.load(file)
            if 'username' in login and 'password' in login :
                username = login['username']
                password = login['password']
            else:
                print('no user')
                return False
            try:
                login_result = self.client.oauth_login(username, password)
                if login_result['success']:
                    token = login_result['token']
                    self.client.blackboard_sso_login(token)
                    return True
                else:
                    print(login_result)
                    return False
            except Exception as e:
                print(e)
                return False

