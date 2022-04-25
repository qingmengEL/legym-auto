import os
import legym_api

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
keyword = os.environ.get('KEYWORD')

uesr = legym_api.login(username, password)
uesr.get_activities()
uesr.signup_activities(keyword)
uesr.signin_activities(keyword)
