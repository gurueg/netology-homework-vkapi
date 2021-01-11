import requests
import json
import time

with open('settings.json') as f:
    json_data = json.load(f)

VERSION = json_data['version']
TOKEN = json_data['token']


class vkUser():
    url = 'https://api.vk.com/method/'
    def __init__(self, user_id, version, token):
        self.user_id = user_id
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version     
        }
        self.data = self.get_user_data(self.user_id)

    def __send_request(self, url, params):
        repeat = True
        while repeat:
            response = requests.get(url, params).json()
            if 'error' in response and 'error_code' in response['error'] and response['error']['error_code'] == 6:
                time.sleep(0.3)
            else:
                repeat = False

        return response['response']

    def get_user_data(self, user_id=None):
        request_params = {**self.params, 'fields':'domain'}
        if user_id is not None:
            request_params = {**request_params, 'user_ids': [user_id]}

        return self.__send_request(self.url+'users.get', request_params)[0]

    def get_common_friends(self, otherUser):
        if isinstance(otherUser, vkUser):
            request_params = {**self.params, 'source_uid': self.user_id, 'target_uid': otherUser.user_id}
            response = self.__send_request( self.url+'friends.getMutual', request_params)

            user_list = []
            for idx in response:
                user_list.append(vkUser(idx, self.version, self.token))  

            return user_list  

    def __and__(self, other):
        return self.get_common_friends(other)

    def __str__(self):
        return 'https://vk.com/' + self.data['domain']
            

def main():
    user1 = vkUser(34604696, VERSION, TOKEN)
    user2 = vkUser(95323557, VERSION, TOKEN)
    
    listcommon = user1.get_common_friends(user2)
    for item in listcommon:
        print(item)

    print('-----')

    listcommon = user1 & user2
    for item in listcommon:
        print(item)


if __name__== "__main__":
    main()
