from tqdm import tqdm
import requests, json,time,os
GET_PHOTOS_URL = 'https://api.vk.com/method/photos.get'
VK_PHOTOS_FOLD = 'download_vkphotos'
BASE_PATH = os.getcwd()
FULL_PATH_TO_VKPHOTOS = os.path.join(BASE_PATH,VK_PHOTOS_FOLD)
LOG_FILE = 'log.json'
FULL_PATH_TOLOG = os.path.join(BASE_PATH,LOG_FILE)
class VK:
    def __init__(self,user_id, token):
        self.token = token
        self.user_id = user_id
        
    def get_photos(self, user_id):
        params = {'access_token': self.token,
                'v':'5.131',
                'album_id': 'profile',
                'owner_id': user_id,
                'extended': True,
                'photo_sizes': True,
                'count': 5,
                'owner_id': user_id
                }
        profile_list = requests.get(GET_PHOTOS_URL, params=params)
        photos_list= []
        if profile_list.status_code == 200:
            print("Success")
            profile_list = profile_list.json()
            for file in tqdm(profile_list['response']['items']):
                time.sleep(3)
                self.size = file['sizes'][-1]['type']
                photo_url = file['sizes'][-1]['url']
                file_name = file['likes']['count']
                download_photo = requests.get(photo_url)
                with open(f'{FULL_PATH_TO_VKPHOTOS}/{file_name}.jpg', 'wb') as f:
                    f.write(download_photo.content)
        else: print('Fail')
        for photo in tqdm(os.listdir(FULL_PATH_TO_VKPHOTOS)): 
            download_log = {'file_name': photo, 'size': self.size}
            photos_list.append(download_log)
        with open(FULL_PATH_TOLOG, "a") as file:
            log_file = json.dump(photos_list, file, indent=3)   
        return log_file