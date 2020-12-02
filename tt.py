import json
import requests
import pandas as pd
from dbconnector import sqlserver

tokens=  pd.read_sql('select * from KakaoAuthInfo',sqlserver).iloc[0].to_dict()




url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
friend_url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

# 사용자 토큰
headers = {
    "Authorization": "Bearer " + tokens['access_token']
}


data = {
    "template_object" : json.dumps({ "object_type" : "text",
                                     "text" : "급등 ㅁㄴㅇㅁㄴ 하이닉스!",
                                     "link" : {
                                                 "web_url" : "www.naver.com"
                                              }
    })
}
data["template_object"]

response = requests.post(url, headers=headers, data=data)

print(response.status_code)
if response.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))