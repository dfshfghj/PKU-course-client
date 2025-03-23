from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget
from .Ui_LoginInterface import Ui_LoginInterface
from .portal_interface import PortalInterface
from qfluentwidgets import FluentIcon
from .. import resources_rc
import json
from ..common.course_requests import Client

class LoginInterface(Ui_LoginInterface, QWidget):
    def __init__(self, client: Client, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.enable_network = True
        self.client = client
        self.background_image = QtGui.QPixmap(":/images/login_background.jpg")
        self.pushButton.clicked.connect(self.login)
        self.exitButton.setIcon(FluentIcon.LEFT_ARROW)
        self.exitButton.setText('使用离线模式')
        self.exitButton.clicked.connect(self.start_without_network)
    def paintEvent(self, a0):
        painter = QtGui.QPainter(self)
        scaled_image = self.background_image.scaled(
            self.size(),
            aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            transformMode=QtCore.Qt.TransformationMode.SmoothTransformation
        )
        painter.drawPixmap(self.rect(), scaled_image)
        return super().paintEvent(a0)
    def login(self):
        print('try login..')
        print(self.parent().parent().parent().portalInterface)
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        print(username, password)
        try:
            login_result = self.client.oauth_login(username, password)
            print(login_result)
            if login_result['success']:
                print('login')
                token = login_result['token']
                self.client.blackboard_sso_login(token)
                with open('data/login.json', 'w', encoding='utf-8') as file:
                    json.dump({
                        'username': username,
                        'password': password
                    }, file)
                portalInterface = PortalInterface(self.client, self.parent())
                self.parent().parent().parent().portalInterface = portalInterface
                self.parent().addWidget(portalInterface)
                self.parent().setCurrentWidget(portalInterface)
                print('next')
                self.parent().parent().parent().portalInterface = portalInterface
            else:
                print(login_result)
                print('fail')
        except Exception as e:
            print(e)
    
    def start_without_network(self):
        portalInterface = PortalInterface(self.client, self.parent())
        self.parent().parent().parent().portalInterface = portalInterface
        self.parent().addWidget(portalInterface)
        self.parent().setCurrentWidget(portalInterface)
        print('start without network')
        self.parent().parent().parent().portalInterface = portalInterface

            
