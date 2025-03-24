from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from .Ui_CourseAnnouncementInterface import Ui_CourseAnnouncementInterface
from .course_content_interface import CourseContentInterface
from qfluentwidgets import FluentIcon, StateToolTip, setCustomStyleSheet
from ..components.card import DocumentCard
from ..common.get_information import getCourseDocuments, uri2id
from ..common.course_requests import Client, Web, detect_type
from ..components.FileDownloader import FileDownloader
import json
from datetime import datetime, timedelta


class CourseAssignmentsInterface(Ui_CourseAnnouncementInterface, QWidget):
    def __init__(self, name: str, id_dict: dict, client: Client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.client = client
        self.name = name
        self.course_id, self.content_id = id_dict['course_id'], id_dict['content_id']
        self.current_time = datetime.now()
        self.stateTooltip = None

        self.init_ui()

        self.load_data()

    def init_ui(self):
        self.img_icon = {
            "内容文件夹": FluentIcon.FOLDER,
            "作业": FluentIcon.DOCUMENT
        }
        self.courseTitleLabel.setText(self.name)
        self.pageTitleHeader.setText('课程作业')

    def load_data(self):
        print('loading data')
        self.loadDataThread = LoadDataThread(
            (self.course_id, self.content_id), self.client, self)
        self.loadDataThread.data_loaded.connect(self.on_data_loaded)
        self.loadDataThread.start()

    def on_data_loaded(self, content):
        print('data_loaded')
        self.content = content
        self.display_data()

    def display_data(self):
        self.assignmentsCards = []
        for assignment in self.content:
            icon = self.img_icon.get(assignment['image'], FluentIcon.DOCUMENT)
            if assignment['details']:
                card = DocumentCard(icon, True, self)
                card.details.setText(assignment['details'])
                card.details.setTextInteractionFlags(
                    Qt.TextInteractionFlag.LinksAccessibleByMouse)
                card.details.linkActivated.connect(self.get_linked_files)
            else:
                card = DocumentCard(icon, False, self)

            card.href = assignment['href']
            card.clicked.connect(
                lambda uri=card.href: self.get_to_new_page(uri))
            card.title.setText(assignment['name'])
            self.assignmentsCards.append(card)
            self.container.addWidget(card)

    def get_linked_files(self, link):
        qss = "StateToolTip {background-color: #AAAAAAAA}"
        if self.stateTooltip is None:
            self.stateTooltip = StateToolTip('下载文件', '下载中...', self)
            setCustomStyleSheet(self.stateTooltip, qss, qss)
            self.stateTooltip.move(self.stateTooltip.getSuitablePos())
            self.stateTooltip.show()
        downloader = FileDownloader(self.client, link, dir='download')
        downloader.finished.connect(lambda: self.finishDownload(downloader))
        downloader.start()

    def finishDownload(self, downloader: FileDownloader):
        downloader.quit()
        downloader.wait()
        if self.stateTooltip:
            self.stateTooltip.setContent('下载完成！')
            self.stateTooltip.setState(True)
            self.stateTooltip = None

    def get_to_new_page(self, uri):
        if detect_type(uri) == Web.COURSE_CONTENT_PAGE:
            id_dict = uri2id(uri)
            if uri in self.parent().parent().page:
                self.parent().parent().stackedWidget.setCurrentWidget(
                    self.parent().parent().page[uri])
            else:
                newCourseContentPage = CourseContentInterface(
                    self.name, id_dict, self.client, self.parent())
                self.parent().parent().stackedWidget.addWidget(newCourseContentPage)
                self.parent().parent().stackedWidget.setCurrentWidget(newCourseContentPage)
                self.parent().parent().page[uri] = newCourseContentPage
        elif detect_type(uri) == None:
            self.get_linked_files(uri)
        else:
            pass


class LoadDataThread(QThread):
    data_loaded = pyqtSignal(list)

    def __init__(self, key: tuple, client, parent=None):
        super().__init__(parent)
        self.course_id, self.content_id = key
        self.client = client
        self.current_time = datetime.now()

    def run(self):
        try:
            with open('data/courseAssignments.json', 'r', encoding='utf-8') as file:
                prev_assignments = json.load(file)
            if not self.course_id in prev_assignments or self.current_time - datetime.strptime(prev_assignments[self.course_id]['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(seconds=1):
                try:
                    assignments_html = self.client.blackboard_course_content_page(
                        self.course_id, self.content_id)
                    self.content = getCourseDocuments(assignments_html)
                    self.update_assignments_json(
                        self.course_id, self.current_time, self.content)
                except:
                    if self.course_id in prev_assignments:
                        self.content = prev_assignments[self.course_id]['content']
                    else:
                        self.content = []
            else:
                self.content = prev_assignments[self.course_id]['content']

        except Exception as e:
            self.content = []
            print(e)
        self.data_loaded.emit(self.content)

    def update_assignments_json(self, key, time, content):
        with open('data/courseAssignments.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[key] = {'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                         'content': content
                         }
            file.seek(0)
            json.dump(data, file)
            file.truncate()
