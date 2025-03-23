from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget, QApplication, QStackedWidget, QStackedLayout
from PyQt6.QtCore import Qt
from .Ui_CourseAnnouncementInterface import Ui_CourseAnnouncementInterface
from qfluentwidgets import BodyLabel, StateToolTip, setCustomStyleSheet
from ..common.course_requests import Client
from ..common.get_information import getTable, getVideoInfo, url2videoInfo
from ..components.AutoAdjustTableWidget import AutoAdjustTableWidget
from ..components.FileDownloader import FileDownloader
import json
import re
from urllib.parse import urljoin
from datetime import datetime, timedelta

class CourseVideoListInterface(Ui_CourseAnnouncementInterface, QWidget):
    def __init__(self, name: str, id_dict: dict, client: Client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.client = client
        self.name = name
        self.key = id_dict['course_id']
        self.current_time = datetime.now()
        self.stateTooltips = {}
        self.init_ui()
        self.load_data()
        self.display_data()

    def init_ui(self):
        self.courseTitleLabel.setText(self.name)
        self.pageTitleHeader.setText('课程回放')

    def load_data(self):
        with open('data/courseVideoList.json', 'r', encoding='utf-8') as file:
            prev_video_list = json.load(file)

        if not self.key in prev_video_list or self.current_time - datetime.strptime(prev_video_list[self.key]['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(seconds=1):
            try:
                video_list_html = self.client.blackboard_course_video_list(self.key)
                self.content = getTable(video_list_html)
                self.update_video_list_json(self.key, self.current_time, self.content)
            except:
                if self.key in prev_video_list:
                    self.content = prev_video_list[self.key]['content']
                else:
                    self.content = [['名称', '时间', '教师', '操作']]
        else:
            self.content = prev_video_list[self.key]['content']

    def display_data(self):
        self.table = AutoAdjustTableWidget(self)
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
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
                label.linkActivated.connect(self.downloadVideo)
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

    def downloadVideo(self, link):
        #print(link)
        link = urljoin('webapps/bb-streammedia-hqy-BBLEARN/', link)
        print(link)
        response = self.client.get_by_uri(link)
        response.raise_for_status()
        video_html = response.text
        #print(video_html)
        src = getVideoInfo(video_html)
        print(src)
        src = src.replace('×', '&times')
        print(src)
        response_2 = self.client.get_by_uri(src)
        response_2.raise_for_status()
        url = response_2.url
        print(url)
        course_id, sub_id, app_id, auth_data = url2videoInfo(url)
        print(course_id, sub_id, app_id, auth_data)
        info_json = self.client.blackboard_course_video_sub_info(course_id, sub_id, app_id, auth_data)
        print(info_json)
        title = info_json['list'][0]['title']
        lecturer_name = info_json['list'][0]['lecturer_name']
        sub_content = json.loads(info_json['list'][0]['sub_content'])
        playback_url = sub_content['save_playback']['contents']
        print(playback_url)
        is_m3u8 = sub_content['save_playback']['is_m3u8']
        if is_m3u8:
            import re
            m3u8_pattern = r"https://resourcese\.pku\.edu\.cn/play/0/harpocrates/\d+/\d+/\d+/([a-zA-Z0-9]+)/\d+/playlist\.m3u8\.*"
            matches = re.match(m3u8_pattern, playback_url)
            hash_value = matches.group(1)
            download_url = f"https://course.pku.edu.cn/webapps/bb-streammedia-hqy-BBLEARN/downloadVideo.action?resourceId={hash_value}"
            self.get_linked_files(download_url, file_name=f"{title} {lecturer_name} {hash_value}.mp4")

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

            


