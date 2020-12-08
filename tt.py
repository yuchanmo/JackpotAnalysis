import json
import requests
import pandas as pd
from dbconnector import sqlserver

tokens=  pd.read_sql('select * from KakaoAuthInfo',sqlserver).iloc[0].to_dict()

code	access_token	refresh_token	expires_in	scope	refresh_token_expires_in
yygT0DEyq_jWZLLmDcf8h5XHOWiwo9B3AdzR0HB9f8dFWfwZ2VTrfwLdtrUWWePf_g7WmgopyNoAAAF2M4Ll9g	s0T3AQLmh5PjCar4XXAFt1b8wV_Ew46w5GuDSQo9c5oAAAF2M4Lpbw	tLcU_xf-KJezvstmsBQeTRNJKcMbk1fFQY-28Ao9c5oAAAF2M4Lpbg	21599	talk_message	5183999
code	access_token	refresh_token	expires_in	scope	refresh_token_expires_in
tTB_xir6V5qw3m9RcEl5UIG1ptxGEn-7esnCYJyXmnaJamSvle1XgcgWdiILPLaSWzSC1Ao9dZwAAAF2M4obbw	TAepjaHRPTQChilPJk37Klv7Remtk7UFVer7kQo9dZwAAAF2M4ocNA	N5PYQtyMNV9nTcxDpdwM6aBa0c7Z3zDDRkS8wAo9dZwAAAF2M4ocMw	21599	talk_message	5183999

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