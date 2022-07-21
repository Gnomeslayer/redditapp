import requests
import json


class Reddit(object):

    def __init__(self, client_id, secret_key, username, password, headers=None, user_info=None):
        self.client_id = client_id
        self.secret_key = secret_key
        self.username = username
        self.password = password
        self.headers = self.get_headers()


    def connect(self):
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret_key)
        data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
            }
        response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=self.headers)
        TOKEN = response.json()['access_token']
        self.headers['Authorization'] = f'bearer {TOKEN}'

    def get_headers(self):
        headers = {
            'User-Agent': 'MyAPI/0.0.1',
            'Authorization': '',
            }
        return headers

    def user_information(self, headers):
        mydata = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
        user_data = {
            'total_karma': mydata.json()['total_karma'],
            'banner_img': mydata.json()['subreddit']['banner_img'],
            'display_name': mydata.json()['name'],
            'icon_img': mydata.json()['icon_img'],
            'inbox_count': mydata.json()['inbox_count']
            }
        return user_data

    def user_inbox(self, headers):
        mydata = requests.get('https://oauth.reddit.com/message/unread', headers=headers)
        mail_data = []
        inboxdata = mydata.json()['data']['children']
        #print(json.dumps(inboxdata, indent = 2))
        for i in range(len(inboxdata)):
            author = inboxdata[i]['data']['author']
            subreddit = inboxdata[i]['data']['subreddit']
            message = inboxdata[i]['data']['body']
            id = inboxdata[i]['data']['name']
            parent = inboxdata[i]['data']['parent_id']
            mail_data.append({
                'author': author,
                'subreddit': subreddit,
                'message': message,
                'id': id,
                'parent_id': parent})
        return mail_data
    
    def mark_read(self, headers, id):
        mydata = requests.post('https://oauth.reddit.com/api/read_message/', data={'id': id},headers=headers)

    def comment_reply(self, headers, comment_id, user_comment):
        mydata = requests.post('https://oauth.reddit.com/api/comment/', data={'thing_id': comment_id, 'text': user_comment},headers=headers)

