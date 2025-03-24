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

        self.init_ui()

        self.load_data()

        self.display_data()
        
    def init_ui(self):
        self.courseTitleLabel.setText(self.name)
        self.pageTitleHeader.setText('公告')

    def load_data(self):
        with open('data/courseAnnouncement.json', 'r', encoding='utf-8') as file:
            prev_announcement = json.load(file)

        if not self.key in prev_announcement or self.current_time - datetime.strptime(prev_announcement[self.key]['time'], "%Y-%m-%d %H:%M:%S") >= timedelta(hours=1):
            try:
                announcement_html = self.client.blackboard_coursepage(self.key)
                self.content = getCourseAnnouncement(announcement_html)
                self.update_announcement_json(self.key, self.current_time, self.content)
            except Exception as e:
                print(e)
                if self.key in prev_announcement:
                    self.content = prev_announcement[self.key]['content']
                else:
                    self.content = []
        else:
            self.content = prev_announcement[self.key]['content']

    def display_data(self):
        self.announcementCards = []
        for announcement in self.content:
            card = AnnouncementCard(self.client.session, self)
            card.addHtml(announcement['content'])
            card.announcementTitleLabel.setText(announcement['title'])
            card.info_1.setText(announcement['poster'])
            card.info_2.setText(announcement['post_to'])
            card.detailsLabel.setText(announcement['time'])
            self.announcementCards.append(card)
            self.container.addWidget(card)

    def update_announcement_json(self, key, time, content):
        with open('data/courseAnnouncement.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data[key] = {'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'content': content
                        }
            file.seek(0)
            json.dump(data, file)
            file.truncate()