from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication, QStackedWidget, QStackedLayout
from PyQt6.QtCore import Qt
from .Ui_CourseAnnouncementInterface import Ui_CourseAnnouncementInterface
from qfluentwidgets import PushButton, TransparentPushButton, TransparentToolButton, FluentIcon, TableWidget, BodyLabel, isDarkTheme
from ..components.card import DocumentCard
from ..common.get_information import getTable
import json
import re
from datetime import datetime, timedelta

class CourseTeachingStaffListInterface(Ui_CourseAnnouncementInterface, QWidget):
    def __init__(self, name: str, id_dict: dict, client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.client = client
        self.name = name
        self.key = id_dict['course_id']
        self.current_time = datetime.now()

        self.init_ui()
        #self.load_data()
        #self.display_data()

    def init_ui(self):
        self.courseTitleLabel.setText(self.name)
        self.pageTitleHeader.setText('教参列表')

    def load_data(self):
        with open('data/courseTeachingStaffList.json', 'r', encoding='utf-8') as file:
            prev_teaching_staff_list = json.load(file)

        if not self.key in prev_teaching_staff_list or self.current_time - datetime.strptime(prev_teaching_staff_list[self.key]['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(seconds=1):
            teaching_staff_list_html = self.client.blackboard_course_video_list(self.key)
            self.content = getTable(teaching_staff_list_html)
            self.update_video_list_json(self.key, self.current_time, self.content)
        else:
            self.content = prev_teaching_staff_list[self.key]['content']

    def display_data(self):
        self.table = TableWidget(self)
        self.table.setRowCount(len(self.content) - 1)
        self.table.setColumnCount(len(self.content[0]))
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setWordWrap(False)
        self.table.setHorizontalHeaderLabels(self.content[0])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.verticalHeader().hide()
        
        for row in range(0, len(self.content) - 1):
            for col in range(len(self.content[0])):
                label = BodyLabel(self.content[row+1][col])
                label.setTextFormat(Qt.TextFormat.RichText)
                label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
                self.table.setCellWidget(row, col, label)
                
        self.table.adjustSize()
        self.table.setObjectName('VideoList')
        self.container.addWidget(self.table)
        
    def update_video_list_json(self, key, time, content):
        with open('data/courseVideoList.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[key] = {'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'content': content
                        }
            file.seek(0)
            json.dump(data, file)
            file.truncate()