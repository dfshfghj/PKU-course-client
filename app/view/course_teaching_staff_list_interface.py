from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget, QStackedWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from .Ui_CourseAnnouncementInterface import Ui_CourseAnnouncementInterface
from qfluentwidgets import TableWidget, BodyLabel, Pivot
from ..common.course_requests import Client
from ..common.get_information import getTables
from ..components.AutoAdjustTableWidget import AutoAdjustTableWidget
import json
from datetime import datetime, timedelta


class CourseTeachingStaffListInterface(Ui_CourseAnnouncementInterface, QWidget):
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
        self.pageTitleHeader.setText('教参列表')
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.container.setContentsMargins(30, 0, 30, 30)
        self.container.addWidget(self.pivot, 0, Qt.AlignmentFlag.AlignLeft)
        self.container.addWidget(self.stackedWidget)
        self.tables = []

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
        self.container.removeWidget(self.loadingLabel)
        self.loadingLabel.hide()
        self.loadingLabel.deleteLater()
        name = ['指定教参列表', '可选教参列表']
        print(self.content)
        for i in range(len(self.content)):
            table = self.content[i]
            tablewidget = AutoAdjustTableWidget(self)
            tablewidget.setRowCount(len(table) - 1)
            tablewidget.setColumnCount(len(table[0]))
            tablewidget.setBorderVisible(True)
            tablewidget.setBorderRadius(8)
            tablewidget.setWordWrap(False)
            tablewidget.setHorizontalHeaderLabels(table[0])
            tablewidget.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeMode.Stretch)
            tablewidget.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
            tablewidget.verticalHeader().setDefaultSectionSize(50)
            tablewidget.verticalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            tablewidget.verticalHeader().hide()

            for row in range(0, len(table) - 1):
                for col in range(len(table[0])):
                    label = BodyLabel(table[row+1][col])
                    label.setTextFormat(Qt.TextFormat.RichText)
                    label.setTextInteractionFlags(
                        Qt.TextInteractionFlag.LinksAccessibleByMouse)
                    label.setWordWrap(True)
                    label.setMinimumHeight(50)
                    label.setContentsMargins(5, 5, 5, 5)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    tablewidget.setCellWidget(row, col, label)

            tablewidget.adjustSize()
            tablewidget.setObjectName('VideoList')
            self.tables.append(tablewidget)
            self.addSubInterface(tablewidget, 'appointTableWidget', name[i])
        if len(self.content):
            self.stackedWidget.setCurrentWidget(self.tables[0])
            self.pivot.setCurrentItem(self.tables[0].objectName())

    def addSubInterface(self, widget: QWidget, objectName: str, text: str):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


class LoadDataThread(QThread):
    data_loaded = pyqtSignal(list)

    def __init__(self, key, client, parent=None):
        super().__init__(parent)
        self.key = key
        self.client = client
        self.current_time = datetime.now()

    def run(self):
        try:
            with open('data/courseTeachingStaffList.json', 'r', encoding='utf-8') as file:
                prev_teaching_staff_list = json.load(file)

            if not self.key in prev_teaching_staff_list or self.current_time - datetime.strptime(prev_teaching_staff_list[self.key]['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(seconds=1):
                try:
                    teaching_staff_list_html = self.client.blackboard_course_teaching_staff(
                        self.key)
                    self.content = getTables(teaching_staff_list_html)
                    self.update_teaching_staff_list_json(
                        self.key, self.current_time, self.content)
                except Exception as e:
                    print(e)
                    if self.key in prev_teaching_staff_list:
                        self.content = prev_teaching_staff_list[self.key]['content']
                    else:
                        self.content = []
            else:
                self.content = prev_teaching_staff_list[self.key]['content']

        except Exception as e:
            self.content = []
            print(e)
        self.data_loaded.emit(self.content)

    def update_teaching_staff_list_json(self, key, time, content):
        with open('data/courseTeachingStaffList.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[key] = {'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                         'content': content
                         }
            file.seek(0)
            json.dump(data, file)
            file.truncate()
