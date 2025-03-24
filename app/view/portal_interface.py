from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QListWidgetItem
from .Ui_PortalInterface import Ui_PortalInterface
from .course_interface import CourseInterface
from PyQt6.QtGui import QFont

from qfluentwidgets import FluentIcon

from ..common.course_requests import Client
from ..common.icons import LocalIcon
from ..common.course_requests import Client
from ..common.get_information import getPortal, simplifyCourseName
import json
from datetime import datetime, timedelta


class PortalInterface(Ui_PortalInterface, QWidget):
    def __init__(self, client: Client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.current_time = datetime.now()
        self.client = client
        self.visited = {}

        self.init_ui()

        self.load_data()

        self.display_data()
        
    def init_ui(self):
        font = QFont()
        font.setBold(True)

        self.currentListWidget.clear()
        self.historyListWidget.clear()

        self.toolButton.setIcon(LocalIcon.PKUFULL)
        self.toolButton.setIconSize(QtCore.QSize(107, 30))
        self.alarm_toolButton.setIcon(FluentIcon.RINGER)

        self.currentListWidget.itemClicked.connect(
            lambda: self.on_listitem_clicked(self.currentListWidget, self.current_courses)
        )
        self.historyListWidget.itemClicked.connect(
            lambda: self.on_listitem_clicked(self.historyListWidget, self.history_courses)
        )

    def load_data(self):
        with open('data/portal.json', 'r', encoding='utf-8') as file:
            prev_home_page = json.load(file)

        if not 'time' in prev_home_page or self.current_time - datetime.strptime(prev_home_page['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(days=30):
            try:
                home_page = self.client.blackboard_homepage()
                (
                    self.current_courses,
                    self.history_courses,
                    self.announcement,
                    self.organization,
                    self.task,
                ) = getPortal(home_page)

                for course in self.current_courses:
                    course['name'] = simplifyCourseName(course['name'])
                for course in self.history_courses:
                    course['name'] = simplifyCourseName(course['name'])

                self.update_portal_json(
                    self.current_time, self.current_courses, self.history_courses, self.announcement, self.organization, self.task
                )
            except Exception:
                if 'time' in prev_home_page:
                    self.current_courses = prev_home_page['current_courses']
                    self.history_courses = prev_home_page['history_courses']
                    self.announcement = prev_home_page['announcement']
                    self.organization = prev_home_page['organization']
                    self.task = prev_home_page['task']
                else:
                    self.current_courses = []
                    self.history_courses = []
                    self.announcement = '无公告'
                    self.organization = '您当前未参加任何组织。'
                    self.task = '我的任务：\n没有到期任务。'
        else:
            self.current_courses = prev_home_page['current_courses']
            self.history_courses = prev_home_page['history_courses']
            self.announcement = prev_home_page['announcement']
            self.organization = prev_home_page['organization']
            self.task = prev_home_page['task']

    def display_data(self):
        font = QFont()
        font.setBold(True)

        for course in self.current_courses:
            item = QListWidgetItem(course['name'])
            item.setFont(font)
            self.currentListWidget.addItem(item)

        for course in self.history_courses:
            item = QListWidgetItem(course['name'])
            item.setFont(font)
            self.historyListWidget.addItem(item)

        self.announcementContent.setText(self.announcement)
        self.organizationContent.setText(self.organization)
        self.taskContent.setText(self.task)      

    def on_listitem_clicked(self, listWidget, data):
        index = listWidget.selectedIndexes()[0].row()
        key = data[index]['key']
        #print(key)
        if not key in self.visited:
            self.visited[key] = CourseInterface(key, self.client, self)
        self.parentWidget().addWidget(self.visited[key])
        self.parentWidget().setCurrentWidget(self.visited[key])

    def update_portal_json(self, time, current_courses, history_courses, announcement, organization, task):
        with open('data/portal.json', 'w', encoding='utf-8') as file:
            json.dump({
                'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                'current_courses': current_courses,
                'history_courses': history_courses,
                'announcement': announcement,
                'organization': organization,
                'task': task
                }, file)
