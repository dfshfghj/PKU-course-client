from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication, QStackedWidget, QStackedLayout
from PyQt6.QtCore import Qt
from .Ui_CourseInterface import Ui_CourseInterface
from .course_announcement_interface import CourseAnnouncementInterface
from .Ui_CourseTeachingStaffListInterface import Ui_CourseTeachingStaffListInterface
from .course_teaching_staff_list_interface import CourseTeachingStaffListInterface
from .course_assignments_interface import CourseAssignmentsInterface
from .course_content_interface import CourseContentInterface
from .course_video_list_interface import CourseVideoListInterface
from .course_grade_interface import CourseGradeInterface
from PyQt6.QtGui import QPixmap, QImage, QPainter, QIcon
from collections import defaultdict
from qfluentwidgets import PushButton, TransparentPushButton, TransparentToolButton, FluentIcon, isDarkTheme

from ..common.course_requests import Client
from ..common.icons import LocalIcon
from ..common.get_information import getCourseAnnouncement, getCourseMenu, uri2id
from ..components.label import CourseMenuLabel

import json


class CourseInterface(Ui_CourseInterface, QWidget):
    def __init__(self, key, client: Client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.key = key
        self.client = client
        with open('data/courseInfo.json', 'r', encoding='utf-8') as file:
            self.course_menu = json.load(file)
        if self.key not in self.course_menu:
            try:
                html = self.client.blackboard_coursepage(key)
                self.course_menu = getCourseMenu(html)
                self.update_course_menu_json()
            except:
                self.course_menu = {
                    'name': 'unknown',
                    'buttons': {},
                    'groups': ['default group']
                }
        else:
            self.course_menu = self.course_menu[self.key]['menu']
        self.course_name = self.course_menu['name']
        self.nav_buttons = self.course_menu['buttons']
        self.groups = self.course_menu['groups']
        self.toolButton.clicked.connect(self.back_to_portal)
        self.myGroupButton.setText(self.groups[0])
        self.courseMenuLabel.setText(self.course_name)
        self.courseMenuLabel.setWordWrap(True)
        self.courseMenu.layout().setSpacing(0)
        self.name_to_button = defaultdict(str, 
        {
            'announcementButton': '课程通知',
            'teachingStaffButton': '课程教参',
            'contentButton': '教学内容',
            'classinButton': '在线课堂',
            'videoButton': '课堂实录',
            'assignmentButton': '课程作业',
            'discussionButton': '答疑讨论',
            'oralTrainingButton': '口语训练',
            'groupButton': '协作小组',
            'blogsButton': '学习日志',
            'classGradeButton': '个人成绩',
            'toolsButton': '教学工具',
            'helpButton': '系统帮助'
        })
        for child in self.courseMenu.findChildren(PushButton):
            nav_button_name = self.name_to_button[child.objectName()]
            if nav_button_name in self.nav_buttons:
                child.uri = self.nav_buttons[nav_button_name]
            else:
                child.uri = None
                self.courseMenu.layout().removeWidget(child)
                child.hide()
                child.deleteLater()
        self.page = {}
        self.pageName = {'announcementButton': CourseAnnouncementInterface,
                         'teachingStaffButton': CourseTeachingStaffListInterface,
                         'assignmentButton': CourseAssignmentsInterface,
                         'contentButton': CourseContentInterface,
                         'videoButton': CourseVideoListInterface,
                         'classGradeButton': CourseGradeInterface
                         }
        self.courseMenuLabel.connectControlWidget(self.courseMenu)
        self.groupMenuLabel.connectControlWidget(self.groupMenu)
        self.toolButton.setIcon(LocalIcon.PKUFULL)
        self.toolButton.setIconSize(QtCore.QSize(107, 30))
        self.alarm_toolButton.setIcon(FluentIcon.RINGER)
        for child in self.courseMenu.findChildren(PushButton):
            child.clicked.connect(lambda checked, button=child: self.go_to_page(button=button))
        try:
            self.go_to_page(self.announcementButton)
            #self.go_to_page(self.nav_buttons[self.name_to_button['announcementButton']], 'announcementButton')
        except:
            pass
    def go_to_page(self, button: QWidget):
        uri = button.uri
        name = button.objectName()
        print(f'go to page: {uri} {name}')
        if uri in self.page:
            print('found')
            self.stackedWidget.setCurrentWidget(self.page[uri])
        else:
            if name in self.pageName:
                print('create new page')
                pageWidget = self.pageName[name](self.course_name, uri2id(uri), self.client, parent=self)
                self.page[uri] = pageWidget
                self.stackedWidget.addWidget(pageWidget)
                self.stackedWidget.setCurrentWidget(pageWidget)

    def back_to_portal(self):
        portalInterface = self.parent().parent().parent().portalInterface
        #self.parent().setCurrentIndex(0)
        self.parent().setCurrentWidget(portalInterface)

    def update_course_menu_json(self):
        with open('data/courseInfo.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[self.key] = {
                        'menu': self.course_menu
                        }
            file.seek(0)
            json.dump(data, file)
            file.truncate()

