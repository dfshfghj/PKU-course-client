import requests
from urllib.parse import urljoin
import json
import os
import random
import threading
import enum

class Web(enum.Enum):
    OAUTH_LOGIN = "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do"
    REDIR_URL = "http://course.pku.edu.cn/webapps/bb-sso-BBLEARN/execute/authValidate/campusLogin"
    SSO_LOGIN = "https://course.pku.edu.cn/webapps/bb-sso-BBLEARN/execute/authValidate/campusLogin"
    BLACKBOARD_HOME_PAGE = "https://course.pku.edu.cn/webapps/portal/execute/tabs/tabAction"
    COURSE_INFO_PAGE = "https://course.pku.edu.cn/webapps/blackboard/execute/announcement"
    COURSE_CONTENT_PAGE = "https://course.pku.edu.cn/webapps/blackboard/content/listContent.jsp"
    COURSE_GRADE_PAGE = "https://course.pku.edu.cn/webapps/bb-mygrades-BBLEARN/myGrades"
    UPLOAD_ASSIGNMENT = "https://course.pku.edu.cn/webapps/assignment/uploadAssignment"
    VIDEO_LIST = "https://course.pku.edu.cn/webapps/bb-streammedia-hqy-BBLEARN/videoList.action"
    VIDEO_SUB_INFO = "https://yjapise.pku.edu.cn/courseapi/v2/schedule/get-sub-info-by-auth-data"


class Client:
    def __init__(self, base_url='https://course.pku.edu.cn'):
        self.base_url = base_url
        self.session = requests.Session()

    def oauth_login(self, username, password):
        response = self.session.post(Web.OAUTH_LOGIN.value, data={
            'appid': 'blackboard',
            'userName': username,
            'password': password,
            'randCode': '',
            'smsCode': '',
            'otpCode': '',
            'redirUrl': Web.REDIR_URL.value
        })
        response.raise_for_status()
        return response.json()

    def blackboard_sso_login(self, token):
        rand = str(random.random())
        response = self.session.get(Web.SSO_LOGIN.value, params={'_rand': rand, 'token': token})
        response.raise_for_status()

    def blackboard_homepage(self):
        response = self.session.get(Web.BLACKBOARD_HOME_PAGE.value, params={'tab_tab_group_id': '_1_1'})
        response.raise_for_status()
        return response.text

    def blackboard_coursepage(self, key):
        response = self.session.get(Web.COURSE_INFO_PAGE.value, params={
            'method': 'search',
            'context': 'course_entry',
            'course_id': key,
            'handle': 'announcements_entry',
            'mode': 'view'
        })
        response.raise_for_status()
        return response.text
    def blackboard_course_content_page(self, course_id, content_id):
        response = self.session.get(Web.COURSE_CONTENT_PAGE.value, params={
            'content_id': content_id,
            'course_id': course_id,
            'mode': 'reset'
        })
        response.raise_for_status()
        return response.text
    def blackboard_course_assignment_uploadpage(self, course_id, content_id):
        response = self.session.get(Web.UPLOAD_ASSIGNMENT.value, params={
            'action': 'newAttempt',
            'content_id': content_id,
            'course_id': course_id
        })
        response.raise_for_status()
        return response.text

    def blackboard_course_assignment_viewpage(self, course_id, content_id):
        response = self.session.get(Web.UPLOAD_ASSIGNMENT.value, params={
            'mode': 'view',
            'content_id': content_id,
            'course_id': course_id
        })
        response.raise_for_status()
        return response.text

    def blackboard_course_assignment_uploaddata(self, multipart_data):
        headers = {
            'origin': 'https://course.pku.edu.cn',
            'accept': '*/*',
            'content-type': multipart_data.content_type
        }
        response = self.session.post(Web.UPLOAD_ASSIGNMENT.value, headers=headers, data=multipart_data.to_string(), params={'action': 'submit'})
        return response
    
    def blackboard_course_grade(self, course_id):
        response = self.session.get(Web.COURSE_GRADE_PAGE.value, params={
                'course_id': course_id,
                'stream_name': 'mygrades',
                'is_stream': False
            })
        response.raise_for_status()
        return response.text
    
    def blackboard_course_video_list(self, course_id):
        response = self.session.get(Web.VIDEO_LIST.value, params={
            'sortDir': 'ASCENDING',
            'numResults': 100,
            'editPaging': 'false',
            'course_id': course_id,
            'mode': 'view',
            'startIndex': 0
        })
        response.raise_for_status()
        return response.text

    def blackboard_course_video_sub_info(self, course_id, sub_id, app_id, auth_data):
        response = self.session.get(Web.VIDEO_SUB_INFO.value, params={
            'all': 1,
            'course_id': course_id,
            'sub_id': sub_id,
            'with_sub_data': 1,
            'app_id': app_id,
            'auth_data': auth_data
        })
        response.raise_for_status()
        return response.json()

    def get_by_uri(self, uri, stream=False, timeout=30):
        if not uri.startswith(('http://', 'https://')):
            url = urljoin('https://course.pku.edu.cn', uri)
        else:
            url = uri
        response = self.session.get(url, stream=stream, timeout=timeout)
        response.raise_for_status()
        return response

    def page_by_uri(self, uri):
        response = self.get_by_uri(uri)
        response.raise_for_status()
        return response.text

def convert_uri(uri, default_scheme="https", default_host="course.pku.edu.cn"):
    if not uri.startswith(('http://', 'https://')):
        uri = f"{default_scheme}://{default_host}{uri}"
    return uri

def detect_type(uri):
    url = convert_uri(uri)
    for web in Web:
        if url.startswith(web.value):
            return web
    return None

class FileDownloader(threading.Thread):
    def __init__(self, client: Client, link, dir):
        super().__init__()
        self.client = client
        self.link = link
        self.dir = dir
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        try:
            response = self.client.get_by_uri(self.link)
            response.raise_for_status()
            file_name = response.url.split("/")[-1]
            with open(os.path.join(self.dir, file_name), 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if self._stop_event.is_set():
                        print("Download interrupted by user.")
                        break
                    if chunk:
                        file.write(chunk)
            if not self._stop_event.is_set():
                print("Download completed successfully.")
            else:
                print("Removing partially downloaded file.")

                os.remove(self.dir)
        except Exception as e:
            print(f"An error occurred during download: {e}")
if __name__ == '__main__':
    client = Client()
    token = client.oauth_login('2400011461', '?zJt31415926!')['token']

