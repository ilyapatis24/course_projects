from tqdm import tqdm
import requests, json,time, os
from vk import VK
MKDIR_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
VK_PHOTOS_FOLD = 'download_vkphotos'
BASE_PATH = os.getcwd()
FULL_PATH_TO_VKPHOTOS = os.path.join(BASE_PATH,VK_PHOTOS_FOLD)
UPLOAD_LINK ='https://cloud-api.yandex.net/v1/disk/resources/upload'
class YandexDisk:
    def __init__(self, token):
        self.token = token
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        
    def create_folder(self,folder):
        requests.put(f'{MKDIR_URL}?path={folder}', headers=self.get_headers())

    def upload_file(self,folder):
        for photo in tqdm(os.listdir(FULL_PATH_TO_VKPHOTOS)):
            time.sleep(3)
            params = {'path': f'{folder}/{photo}', 'overwrite': False}
            get_upload_url = requests.get(UPLOAD_LINK, headers=self.get_headers(), params=params)
            get_url = get_upload_url.json()
            upload_url = get_url['href']
            file_upload = requests.api.put(upload_url, data=open(f'{FULL_PATH_TO_VKPHOTOS}/{photo}', 'rb'), headers=self.get_headers())
            file_upload.raise_for_status()
            if file_upload.status_code == 201:
                print("Success")
            else: print('Fail')