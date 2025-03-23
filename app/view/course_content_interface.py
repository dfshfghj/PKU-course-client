from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from .Ui_CourseAnnouncementInterface import Ui_CourseAnnouncementInterface
from qfluentwidgets import FluentIcon, StateToolTip, setCustomStyleSheet
from ..components.card import DocumentCard
from ..common.get_information import getCourseDocuments, getPageTitle, uri2id
from ..common.course_requests import Web, Client, detect_type
from ..components.FileDownloader import FileDownloader
import json
from datetime import datetime, timedelta


class CourseContentInterface(Ui_CourseAnnouncementInterface, QWidget):
    def __init__(self, name: str, id_dict: dict, client: Client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.client = client
        self.name = name
        self.course_id, self.content_id = id_dict['course_id'], id_dict['content_id']
        self.current_time = datetime.now()
        self.stateTooltips = {}
        self.init_ui()
        self.load_data()
        self.display_data()

    def init_ui(self):
        self.img_icon = {
            "内容文件夹": FluentIcon.FOLDER,
            "作业": FluentIcon.DOCUMENT
        }
        self.courseTitleLabel.setText(self.name)

    def load_data(self):
        with open('data/courseContent.json', 'r', encoding='utf-8') as file:
            prev_contents = json.load(file)
        if not self.course_id in prev_contents or not self.content_id in prev_contents[self.course_id] or self.current_time - datetime.strptime(prev_contents[self.course_id][self.content_id]['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(seconds=1):
            try:
                content_html = self.client.blackboard_course_content_page(self.course_id, self.content_id)
                self.content = getCourseDocuments(content_html)
                self.pageTitleHeader.setText(getPageTitle(content_html))
                self.update_content_json(
                    self.course_id, self.content_id, self.current_time, self.content)
            except Exception as e:
                if self.course_id in prev_contents and self.content_id in prev_contents[self.course_id]:
                    self.content = prev_contents[self.course_id][self.content_id]['content']
                    self.pageTitleHeader.setText(prev_contents[self.course_id][self.content_id]['title'])
                else:
                    self.content = []
        else:
            print(1)
            self.content = prev_contents[self.course_id][self.content_id]['content']
            self.pageTitleHeader.setText(prev_contents[self.course_id][self.content_id]['title'])
        

    def display_data(self):
        self.documentCards = []
        for content in self.content:
            icon = self.img_icon.get(content['image'], FluentIcon.DOCUMENT)
            if content['details']:
                card = DocumentCard(icon, True, self)
                card.details.setText(content['details'])
                card.details.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
                card.details.linkActivated.connect(self.get_linked_files)
            else:
                card = DocumentCard(icon, False, self)
            card.title.setText(content['name'])
            card.clicked.connect(lambda link=content['href']: self.get_linked_files(link=link))
            self.documentCards.append(card)
            self.container.addWidget(card)

    def update_content_json(self, course_id, content_id, time, content):
        with open('data/courseContent.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            if course_id  not in data:
                data[course_id] = {}
            data[course_id][content_id] = {'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'content': content
                        }
            file.seek(0)
            json.dump(data, file)
            file.truncate()
    
    def get_linked_files(self, link, file_name=None):
        qss = "StateToolTip {background-color: #AAAAAAAA}"
        if link not in self.stateTooltips:
        #if self.stateTooltips is None:
            stateTooltip = StateToolTip('下载文件', '下载中...', self)
            setCustomStyleSheet(stateTooltip, qss, qss)
            stateTooltip.move(stateTooltip.getSuitablePos())
            stateTooltip.show()
            self.stateTooltips[link] = stateTooltip
        downloader = FileDownloader(self.client, link, dir='download', file_name=file_name)
        downloader.finished.connect(lambda: self.finishDownload(downloader))
        downloader.progress.connect(lambda progress: self.updateDownloadState(link=downloader.link, progress=progress))
        downloader.start()

    def finishDownload(self, downloader: FileDownloader):
        downloader.quit()
        downloader.wait()
        if downloader.link in self.stateTooltips:
        #if self.stateTooltip:
            stateTooltip = self.stateTooltips[downloader.link]
            stateTooltip.setContent('下载完成！')
            stateTooltip.setState(True)
            stateTooltip = None
            self.stateTooltips.pop(downloader.link, None)

    def updateDownloadState(self, link, progress):
        if link in self.stateTooltips:
        #if self.stateTooltip:
            self.stateTooltips[link].setContent(f'下载中...  下载进度：{progress}%')
    
    def get_to_new_page(self, uri):
        if detect_type(uri) == Web.COURSE_CONTENT_PAGE:
            id_dict = uri2id(uri)
            if uri in self.parent().page:
                self.parent().stackedWidget.setCurrentWidget(self.parent().page[uri])
            else:
                newCourseContentPage = CourseContentInterface(self.name, id_dict, self.client, self.parent())
                self.parent().stackedWidget.addWidget(newCourseContentPage)
                self.parent().stackedWidget.setCurrentWidget(newCourseContentPage)
                self.parent().page[uri] = newCourseContentPage
        elif detect_type(uri) == None:
            self.get_linked_files(uri)
        else:
            pass