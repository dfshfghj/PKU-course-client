from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication, QStackedWidget, QStackedLayout, QListWidgetItem
from PyQt6.QtCore import Qt
from .Ui_PortalInterface import Ui_PortalInterface
from .course_interface import CourseInterface
from PyQt6.QtGui import QPixmap, QImage, QPainter, QIcon, QFont

from qfluentwidgets import PushButton, TransparentPushButton, TransparentToolButton, FluentIcon, isDarkTheme

from ..common.qss_management import add_qss
from ..common.course_requests import Client
from ..common.icons import LocalIcon
from ..components.button import PKULogoButton, NavigationButton
from ..common.course_requests import Client
from ..common.get_information import getCourseList, simplifyCourseName
import json
from datetime import datetime, timedelta


class PortalInterface(Ui_PortalInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.current_time = datetime.now()
        self.client = Client()
        token = self.client.oauth_login('2400011461', '?zJt31415926!')['token']
        self.client.blackboard_sso_login(token)
        with open('data/portal.json', 'r', encoding='utf-8') as file:
            prev_home_page = json.load(file)
        font = QFont()
        font.setBold(True)
        self.visited = {}
        self.listWidget.clear()
        self.listWidget_2.clear()
        if not 'time' in prev_home_page or self.current_time - datetime.strptime(prev_home_page['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(days=30):
                home_page = self.client.blackboard_homepage()
                self.current_courses, self.history_courses = getCourseList(home_page)
                for course in self.current_courses:
                    course['name'] = simplifyCourseName(course['name'])
                for course in self.history_courses:
                    course['name'] = simplifyCourseName(course['name'])
                self.update_portal_json(self.current_time, self.current_courses, self.history_courses)
        else:
            self.current_courses = prev_home_page['current_courses']
            self.history_courses = prev_home_page['history_courses']
        for course in self.current_courses:
            item = QListWidgetItem(course['name'])
            item.setFont(font)
            self.listWidget.addItem(item)
        for course in self.history_courses:
            item = QListWidgetItem(course['name'])
            item.setFont(font)
            self.listWidget_2.addItem(item)
        self.parent = parent
        self.toolButton.setIcon(LocalIcon.PKUFULL)
        self.toolButton.setIconSize(QtCore.QSize(107, 30))
        self.alarm_toolButton.setIcon(FluentIcon.RINGER)
        self.listWidget.itemClicked.connect(self.on_listitem_clicked)
    def on_listitem_clicked(self):
        index = self.listWidget.selectedIndexes()[0].row()
        key = self.current_courses[index]['key']
        #print(key)
        if not key in self.visited:
            self.visited[key] = CourseInterface(key, self.client, self)
        self.parentWidget().addWidget(self.visited[key])
        self.parentWidget().setCurrentWidget(self.visited[key])
    def update_portal_json(self, time, current_courses, history_courses):
        with open('data/portal.json', 'w', encoding='utf-8') as file:
            json.dump({'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'current_courses': current_courses,
                        'history_courses': history_courses}, file)


if __name__ == '__main__':
    
    import sys
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    w = PortalInterface()
    w.show()
    app.exec()
