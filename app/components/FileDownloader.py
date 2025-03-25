from PyQt6.QtCore import QThread, pyqtSignal
from ..common.course_requests import Client
import os
import urllib.parse


class FileDownloader(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self, client: Client, link, dir, file_name = None):
        super().__init__()
        self.client = client
        self.link = link
        self.dir = dir
        self.file_name = file_name

    def run(self):
        try:
            response = self.client.get_by_uri(self.link, stream=True)
            response.raise_for_status()
            if self.file_name is None:
                file_name = urllib.parse.unquote(response.url.split("/")[-1])
            else:
                file_name = self.file_name
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            with open(os.path.join(self.dir, file_name), 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)

                        if total_size > 0:
                            progress = int(downloaded_size / total_size * 100)
                            self.progress.emit(progress)

            print("Download completed successfully.")
            response.close()
        except Exception as e:
            print(f"An error occurred during download: {e}")
        self.finished.emit()
        