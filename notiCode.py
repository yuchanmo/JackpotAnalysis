from dbconnector import sqlserver
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime as dt
import numpy as np
import requests
 
print('=================add result=======================')
summary_df.to_sql('Summary',sqlserver,'dbo',index=False,if_exists="append")
summary_df = summary_df.sort_values(by=['coef_cur_trade_volume','coef_trade_price'],ascending=False)
msg ='<1분전 대비 시세>\n'
for i,row in summary_df.iterrows():
    msg = msg + f"[COIN종목] : {row['market']} - [거래량] : {row['cur_trade_volume']} - [물량 증가량] : {round(row['coef_cur_trade_volume'],1)}배 - [가격 증가(%)] : {round(row['coef_trade_price']*100,1)}%\n"        
t = '1625539842:AAE9yZyi2Fe1U3W7j6Yy-XA5ghkWqdc_q4M'    
c_id = '@cocoinmaster'
# bot = telegram.Bot(token=t)
# bot.sendMessage(chat_id=c_id,text=msg)    
url = f'https://api.telegram.org/bot{t}/sendMessage?chat_id={c_id}&text={msg}'
requests.get(url)