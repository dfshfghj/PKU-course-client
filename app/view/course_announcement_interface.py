from PyQt6.QtWidgets import QWidget
from .Ui_CourseAnnouncementInterface import Ui_CourseAnnouncementInterface
from ..components.card import AnnouncementCard
from ..common.get_information import getCourseAnnouncement
import json
from datetime import datetime, timedelta


class CourseAnnouncementInterface(Ui_CourseAnnouncementInterface, QWidget):
    def __init__(self, name: str, id_dict: dict, client, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.client = client
        self.name = name
        self.key = id_dict['course_id']
        self.current_time = datetime.now()
        with open('data/courseAnnouncement.json', 'r', encoding='utf-8') as file:
            prev_announcement = json.load(file)
        if not self.key in prev_announcement or self.current_time - datetime.strptime(prev_announcement[self.key]['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(hours=1):
            try:
                announcement_html = self.client.blackboard_coursepage(self.key)
                self.content = getCourseAnnouncement(announcement_html)
                self.update_announcement_json(self.key, self.current_time, self.content)
            except:
                if self.key in prev_announcement:
                    self.content = prev_announcement[self.key]['content']
                else:
                    self.content = []
        else:
            self.content = prev_announcement[self.key]['content']
        self.announcementCards = []
        self.courseTitleLabel.setText(self.name)
        self.pageTitleHeader.setText('公告')
        for announcement in self.content:
            self.announcementCards.append(AnnouncementCard(self.client.session, self))
            self.announcementCards[-1].addHtml(announcement['content'])
            self.announcementCards[-1].announcementTitleLabel.setText(announcement['title'])
            self.announcementCards[-1].info_1.setText(announcement['poster'])
            self.announcementCards[-1].info_2.setText(announcement['post_to'])
            self.announcementCards[-1].detailsLabel.setText(announcement['time'])
            self.container.addWidget(self.announcementCards[-1])
    
    def update_announcement_json(self, key, time, content):
        with open('data/courseAnnouncement.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[key] = {'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'content': content
                        }
            file.seek(0)
            json.dump(data, file)
            file.truncate()