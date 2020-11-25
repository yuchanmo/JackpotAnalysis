# 참고사항 : 
# Access Token 받는 방법 : https://ai-creator.tistory.com/170
# 메세지 보내는 방법 :  https://ai-creator.tistory.com/23
# https://kauth.kakao.com/oauth/authorize?client_id=fe34e2af8f566373b56dd11318e44207&response_type=code&redirect_uri=https://www.google.com
# code
import json
import requests

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : "fe34e2af8f566373b56dd11318e44207",
    "redirect_uri" : "https://www.google.com",
    "code"         : "YynqOi9TZjMqxAvTTBhG2j1yUDsm7SytVuhOTCoCh3hqwZgK8IHMFLdMndKeLNh37HqOTgo9cxcAAAF0jSSmKg"
    
}
response = requests.post(url, data=data)

tokens = response.json()
with open("kakao_token.json", "w") as fp:
    json.dump(tokens, fp)
print(tokens)

# #refresh
# {
#     "access_token": "wBjmnOALu0rCLYWuc4kPKY5GCstVpT_D9l1L2gopyWAAAAF0TyC28A",
#     "token_type": "bearer",
#     "refresh_token": "y6TNPZZasxAIIAu_vOS3lWKjZRBiDA9TWpse1wopyWAAAAF0TyC27g",
#     "expires_in": 21599,
#     "scope": "talk_message",
#     "refresh_token_expires_in": 5183999
# }

# url = "https://kauth.kakao.com/oauth/token"
# data = {
#     "grant_type" : "refresh_token",
#     "client_id"  : "c41274663b2adca6f0866cb814c0163a",
#     "refresh_token" : "y6TNPZZasxAIIAu_vOS3lWKjZRBiDA9TWpse1wopyWAAAAF0TyC27g"
# }
# response = requests.post(url, data=data)

# print(response.json())

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
friend_url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

# 사용자 토큰
headers = {
    "Authorization": "Bearer " + tokens['access_token']
}


data = {
    "template_object" : json.dumps({ "object_type" : "text",
                                     "text" : "Hello, world!",
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