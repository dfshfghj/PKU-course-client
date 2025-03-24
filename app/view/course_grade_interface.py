from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from .Ui_CourseAnnouncementInterface import Ui_CourseAnnouncementInterface
from qfluentwidgets import BodyLabel, setCustomStyleSheet
from ..common.get_information import getGradeTable
from ..components.AutoAdjustTableWidget import AutoAdjustTableWidget
from ..common.course_requests import Client
import json
from datetime import datetime, timedelta


class CourseGradeInterface(Ui_CourseAnnouncementInterface, QWidget):
    def __init__(self, name: str, id_dict: dict, client: Client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.client = client
        self.name = name
        self.key = id_dict['course_id']
        self.current_time = datetime.now()

        self.init_ui()

        self.load_data()

    def init_ui(self):
        self.courseTitleLabel.setText(self.name)
        self.pageTitleHeader.setText('我的成绩')

    def load_data(self):
        print('loading data')
        self.loadDataThread = LoadDataThread(self.key, self.client, self)
        self.loadDataThread.data_loaded.connect(self.on_data_loaded)
        self.loadDataThread.start()

    def on_data_loaded(self, content):
        print('data_loaded')
        self.content = content
        self.display_data()

    def display_data(self):
        self.table = AutoAdjustTableWidget(self)
        self.table.setRowCount(len(self.content) - 1)
        self.table.setColumnCount(len(self.content[0]) - 1)
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setWordWrap(False)
        header_font = QFont()
        header_font.setBold(True)
        self.table.setHorizontalHeaderLabels(self.content[0][:-1])
        self.table.horizontalHeader().setFont(header_font)
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.table.verticalHeader().setDefaultSectionSize(100)
        self.table.verticalHeader().hide()
        qss = "BodyLabel {margin: 15px}"
        for row in range(0, len(self.content) - 1):
            for col in range(len(self.content[0]) - 1):
                label = BodyLabel(self.content[row+1][col])
                setCustomStyleSheet(label, qss, qss)
                label.setTextFormat(Qt.TextFormat.AutoText)
                label.setTextInteractionFlags(
                    Qt.TextInteractionFlag.LinksAccessibleByMouse)
                self.table.setCellWidget(row, col, label)

        self.table.adjustSize()
        self.table.setObjectName('Grade')
        self.container.addWidget(self.table)


class LoadDataThread(QThread):
    data_loaded = pyqtSignal(list)

    def __init__(self, key, client, parent=None):
        super().__init__(parent)
        self.key = key
        self.client = client
        self.current_time = datetime.now()

    def run(self):
        try:
            with open('data/courseGrade.json', 'r', encoding='utf-8') as file:
                prev_grade = json.load(file)

            if not self.key in prev_grade or self.current_time - datetime.strptime(prev_grade[self.key]['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(seconds=1):
                try:
                    grade_html = self.client.blackboard_course_grade(self.key)
                    self.content = getGradeTable(grade_html)
                    self.update_grade_json(
                        self.key, self.current_time, self.content)
                except:
                    if self.key in prev_grade:
                        self.content = prev_grade[self.key]['content']
                    else:
                        self.content = [['项目', '最新活动', '成绩', '状态']]
            else:
                self.content = prev_grade[self.key]['content']

        except Exception as e:
            self.content = []
            print(e)
        self.data_loaded.emit(self.content)

    def update_grade_json(self, key, time, content):
        with open('data/courseGrade.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[key] = {'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                         'content': content
                         }
            file.seek(0)
            json.dump(data, file)
            file.truncate()
