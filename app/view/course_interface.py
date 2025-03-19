from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication, QStackedWidget, QStackedLayout
from PyQt6.QtCore import Qt
from .Ui_CourseInterface import Ui_CourseInterface
from .course_announcement_interface import CourseAnnouncementInterface
from .Ui_CourseTeachingStaffListInterface import Ui_CourseTeachingStaffListInterface
from .course_assignments_interface import CourseAssignmentsInterface
from .course_content_interface import CourseContentInterface
from .course_video_list_interface import CourseVideoListInterface
from PyQt6.QtGui import QPixmap, QImage, QPainter, QIcon
from collections import defaultdict
from qfluentwidgets import PushButton, TransparentPushButton, TransparentToolButton, FluentIcon, isDarkTheme

from ..common.qss_management import add_qss
from ..common.course_requests import Client
from ..common.icons import LocalIcon
from ..common.get_information import getCourseAnnouncement, getCourseMenu
from ..components.label import CourseMenuLabel


class CourseTeachingStaffListInterface(Ui_CourseTeachingStaffListInterface, QWidget):
    def __init__(self, name: tuple, client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

class CourseInterface(Ui_CourseInterface, QWidget):
    def __init__(self, key, client: Client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.key = key
        self.client = client
        html = self.client.blackboard_coursepage(key)
        self.course_menu = getCourseMenu(html)
        self.course_name = self.course_menu['name']
        self.nav_buttons = self.course_menu['buttons']
        self.nav_urls = self.course_menu['urls']
        self.groups = self.course_menu['groups']
        self.myGroupButton.setText(self.groups[0])
        self.courseMenuLabel.setText(self.course_name)
        self.courseMenuLabel.setWordWrap(True)
        self.courseMenu.layout().setSpacing(0)
        self.name_to_button = defaultdict(str, 
        {
            '课程通知': 'announcementButton',
            '课程教参': 'teachingStaffButton',
            '教学内容': 'contentButton',
            '在线课堂': 'classinButton',
            '课堂实录': 'videoButton',
            '课程作业': 'assignmentButton',
            '答疑讨论': 'discussionButton',
            '口语训练': 'oralTrainingButton',
            '协作小组': 'groupButton',
            '学习日志': 'blogsButton',
            '个人成绩': 'classGradeButton',
            '教学工具': 'toolsButton',
            '系统帮助': 'helpButton'
        })
        self.used_button = set([])
        for name in self.nav_buttons:
            self.used_button.add(self.name_to_button[name])
        for child in self.courseMenu.findChildren(QWidget):
            if child.objectName() not in self.used_button:
                self.courseMenu.layout().removeWidget(child)
                child.hide()
                child.deleteLater() 
        self.page = {}
        self.pageName = {'announcementButton': CourseAnnouncementInterface,
                         'teachingStaffButton': CourseTeachingStaffListInterface,
                         'assignmentButton': CourseAssignmentsInterface,
                         'contentButton': CourseContentInterface,
                         'videoButton': CourseVideoListInterface
                         }
        self.courseMenuLabel.connectControlWidget(self.courseMenu)
        self.groupMenuLabel.connectControlWidget(self.groupMenu)
        self.toolButton.setIcon(LocalIcon.PKUFULL)
        self.toolButton.setIconSize(QtCore.QSize(107, 30))
        self.alarm_toolButton.setIcon(FluentIcon.RINGER)
        self.announcementButton.clicked.connect(lambda: self.go_to_page(name='课程通知'))
        self.teachingStaffButton.clicked.connect(lambda: self.go_to_page(name='课程教参'))
        self.assignmentButton.clicked.connect(lambda: self.go_to_page(name='课程作业'))
        self.contentButton.clicked.connect(lambda: self.go_to_page(name='教学内容'))
        self.videoButton.clicked.connect(lambda: self.go_to_page(name='课堂实录'))
        self.go_to_page('课程通知')
    def go_to_page(self, name):
        print(f'go to page: {name}')
        if name in self.page:
            print('found')
            self.stackedWidget.setCurrentWidget(self.page[name])
        else:
            print('create new')
            pageWidget = self.pageName[self.name_to_button[name]]((self.nav_urls[name], self.course_name), self.client)
            self.page[name] = pageWidget
            self.stackedWidget.addWidget(pageWidget)
            self.stackedWidget.setCurrentWidget(pageWidget)

