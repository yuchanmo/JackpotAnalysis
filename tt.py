# import json
# import requests
# import pandas as pd
# from dbconnector import sqlserver

# tokens=  pd.read_sql('select * from KakaoAuthInfo',sqlserver).iloc[0].to_dict()

# code	access_token	refresh_token	expires_in	scope	refresh_token_expires_in
# yygT0DEyq_jWZLLmDcf8h5XHOWiwo9B3AdzR0HB9f8dFWfwZ2VTrfwLdtrUWWePf_g7WmgopyNoAAAF2M4Ll9g	s0T3AQLmh5PjCar4XXAFt1b8wV_Ew46w5GuDSQo9c5oAAAF2M4Lpbw	tLcU_xf-KJezvstmsBQeTRNJKcMbk1fFQY-28Ao9c5oAAAF2M4Lpbg	21599	talk_message	5183999
# code	access_token	refresh_token	expires_in	scope	refresh_token_expires_in
# tTB_xir6V5qw3m9RcEl5UIG1ptxGEn-7esnCYJyXmnaJamSvle1XgcgWdiILPLaSWzSC1Ao9dZwAAAF2M4obbw	TAepjaHRPTQChilPJk37Klv7Remtk7UFVer7kQo9dZwAAAF2M4ocNA	N5PYQtyMNV9nTcxDpdwM6aBa0c7Z3zDDRkS8wAo9dZwAAAF2M4ocMw	21599	talk_message	5183999

# url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
# friend_url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

# # 사용자 토큰
# headers = {
#     "Authorization": "Bearer " + tokens['access_token']
# }


# data = {
#     "template_object" : json.dumps({ "object_type" : "text",
#                                      "text" : "급등 ㅁㄴㅇㅁㄴ 하이닉스!",
#                                      "link" : {
#                                                  "web_url" : "www.naver.com"
#                                               }
#     })
# }
# data["template_object"]

# response = requests.post(url, headers=headers, data=data)

# print(response.status_code)
# if response.json().get('result_code') == 0:
#     print('메시지를 성공적으로 보냈습니다.')
# else:
#     print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


#%%

from scipy.signal import argrelextrema
import pandas as pd
from dbconnector import sqlserver
from datetime import datetime
import matplotlib.pyplot as plt
from etlhelper import *
import numpy as np



print('start to find jackpot item')
# sql = '''
# select c.name,p.code,p.curval,p.curvol,p.Regdate
#   from Stock.dbo.AllTimePriceFromNaver p
#   join code c
# 	on p.code = c.code
#   where Regdate >= DATEADD(MINUTE,-10,getdate())
# '''

fromstr = datetime.today().strftime('%Y-%m-%d')
#fromstr = '2020-12-10'

sql = f'''
select c.name,p.code,p.startval, p.curval,p.curvol,p.Regdate
    from Stock.dbo.AllTimePriceFromNaver p
    join code c
    on p.code = c.code 
    where Regdate >='{fromstr}'
    order by Regdate desc
    '''

print(sql)
df = pd.read_sql(sql,sqlserver)
init_df = df[df['curvol']>0].groupby(['code'])['curvol'].min().reset_index().rename(columns={'curvol':'startvol'})
df = pd.merge(df,init_df,left_on=['code'],right_on=['code'],how='inner')
# cols = list(df)
# cols.remove('code')
# df = df.groupby(['code']).apply(lambda x : x[cols].tail(100)).reset_index()
df['Regdate'] = pd.to_datetime(df['Regdate'])    
df = df.set_index(['Regdate'])

sdf = df[df['name']=='현대바이오']
#%%

sdf.head()
# %%
sdf['curval'].plot()
#%%
sdf = sdf.sort_index(ascending=True)
# %%


ss.head()
# %%

ss['curval'].plot()
# %%
ss.head()
# %%

ss[:15]['curval'].plot()
# %%

# %%
np.polyfit(x,y,3)
# %%
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

ss = sdf['2020-12-14 14:10':'2020-12-14 14:13']
ss['curval'].plot()
plt.show()

y = ss['curval'].values
x = np.arange(0,len(y))
X = x.reshape(-1,1)
res = []
for degree in range(1,5):    
    polyreg=make_pipeline(PolynomialFeatures(degree),LinearRegression())
    polyreg.fit(X,y)
    d = degree
    c = polyreg[1].coef_
    res.append((d,c[-1]))
    ypred = polyreg.predict(X)
    plt.title(title)
    plt.plot(x,y)
    plt.plot(x,ypred,'-')
    plt.show()
    print(mean_squared_error(ypred,y))
print(res)
    


len(ss)
for degree in range(1,5):
    polyreg=make_pipeline(PolynomialFeatures(degree),LinearRegression())
    polyreg.fit(X,y)
    d = degree
    c = polyreg[1].coef_
    res.append((d,c[-1]))
    ypred = polyreg.predict(X)
    plt.title(title)
    plt.plot(x,y)
    plt.plot(x,ypred,'-')
    plt.show()
    print(mean_squared_error(ypred,y))

res