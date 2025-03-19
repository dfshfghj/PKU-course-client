from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication, QStackedWidget, QStackedLayout
from PyQt6.QtCore import Qt
from .Ui_CourseAnnouncementInterface import Ui_CourseAnnouncementInterface
from qfluentwidgets import PushButton, TransparentPushButton, TransparentToolButton, FluentIcon, isDarkTheme
from ..components.card import DocumentCard
from ..common.get_information import getCourseDocuments
import json
from datetime import datetime, timedelta


class CourseContentInterface(Ui_CourseAnnouncementInterface, QWidget):
    def __init__(self, name: tuple, client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.client = client
        self.url, self.name = name
        self.current_time = datetime.now()

        self.init_ui()
        self.load_data()
        self.display_data()

    def init_ui(self):
        self.img_icon = {
            "内容文件夹": FluentIcon.FOLDER,
            "作业": FluentIcon.DOCUMENT
        }
        self.courseTitleLabel.setText(self.name)
        self.pageTitleHeader.setText('教学内容')

    def load_data(self):
        with open('data/courseAssignments.json', 'r', encoding='utf-8') as file:
            prev_assignments = json.load(file)

        if not self.url in prev_assignments or self.current_time - datetime.strptime(prev_assignments[self.url]['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(seconds=1):
            assignments_html = self.client.page_by_uri(self.url)
            self.content = getCourseDocuments(assignments_html)
            self.update_assignments_json(
                self.url, self.current_time, self.content)
        else:
            self.content = prev_assignments[self.url]['content']

    def display_data(self):
        self.assignmentsCards = []
        for assignments in self.content:
            icon = self.img_icon.get(assignments['image'], FluentIcon.DOCUMENT)
            if assignments['details']:
                card = DocumentCard(icon, True, self)
                card.details.setText(assignments['details'])
            else:
                card = DocumentCard(icon, False, self)
            card.title.setText(assignments['name'])
            self.assignmentsCards.append(card)
            self.container.addWidget(card)

    def update_assignments_json(self, key, time, content):
        with open('data/courseContent.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[key] = {'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                         'content': content
                         }
            file.seek(0)
            json.dump(data, file)
