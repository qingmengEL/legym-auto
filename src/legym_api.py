import json
import requests

base_url = 'https://cpes.legym.cn'

login_url = base_url + '/authorization/user/manage/login'
get_activity_url = base_url + '/education/app/activity/getActivityList'
signup_activity_url = base_url + '/education/app/activity/signUp'
signin_activity_url = base_url + '/education/activity/app/attainability/sign'

headers = {
    'Content-Type': 'application/json'
}


def req(method, url, headers, data, error_text=''):
    response = requests.request(method=method, url=url, headers=headers, data=data)
    if response.status_code != 200:
        print(response.text)
        raise Exception(error_text)
    else:
        return json.loads(response.text)


def login(username, password):
    payload = json.dumps({
        'userName': username,
        'password': password,
        'entrance': 1
    })
    response = req(method='POST', url=login_url, headers=headers, data=payload, error_text='登陆出错')
    return User(response['data']['accessToken'], response['data']['id'])


class User:
    def __init__(self, access_token, user_id):
        self.activities = []
        self.headers = headers
        self.access_token = access_token
        self.headers['Authorization'] = 'Bearer ' + access_token
        self.user_id = user_id

    def get_activities(self):
        payload = json.dumps({
            "name": "",
            "campus": "",
            "page": 1,
            "size": 999,
            "state": "",
            "topicId": "",
            "week": ""
        })
        response = req(method='POST', url=get_activity_url, headers=self.headers, data=payload, error_text='获取活动列表失败')
        self.activities = response['data']['items']

    def signup_activities(self, keyword):
        for activity in self.activities:
            if keyword in activity['name']:
                payload = json.dumps({
                    'activityId': activity['id']
                })
                response = req(method='POST', url=signup_activity_url, headers=self.headers, data=payload,
                               error_text='活动报名失败')

    def signin_activities(self, keyword):
        for activity in self.activities:
            if keyword in activity['name']:
                payload = json.dumps({
                    'userId': self.user_id,
                    'activityId': activity['id'],
                    'pageType': 'activity',
                    'times': 2,
                    'activityType': 0,
                    'attainabilityType': 2
                })
                response = req(method='PUT', url=signin_activity_url, headers=self.headers, data=payload,
                               error_text='活动签到失败')
                print(response)
