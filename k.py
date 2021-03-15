from dbconnector import sqlserver
import pandas as pd
from commonquery import *
from etlhelper import *
import multiprocessing
import asyncio
import parmap
import sys
import requests
import json

#def getDailyStockValue(code,page_limit:int = 50):
code = '000020'
df = pd.DataFrame()
headers = {
  'authority':'finance.naver.com'
  ,'method':'GET'
  ,'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
  ,'accept-encoding' : 'gzip, deflate, br'
  ,'cookie':'NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; NNB=BBPX6MHUJWQV6; MM_NEW=1; NFS=2; MM_NOW_COACH=1; nx_ssl=2; JSESSIONID=9053C395F8362E792978F94FE1B6CAC7'
  ,'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Mobile Safari/537.36'
 ,


}


aa = pd.read_html('https://m.stock.naver.com/item/main.nhn#/stocks/005930/price')
code = '299170'
a = requests.get(f'https://m.stock.naver.com/api/item/getPriceDayList.nhn?code={code}&pageSize=100&page=1')
res = json.loads(a.content)
rows = res['result']['list']
cols = ['date','closeprice','rf','pricediff','cr','openprice','highprice','lowprice','volume']
df = pd.DataFrame(rows)
df.columns = cols
df = df.drop(columns=['rf','cr'])
df['date'] = pd.to_datetime(df['date'])
df['code'] = code

mintime,maxtime =  df.date.min(),df.date.max()
mintimestr,maxtimestr = mintime.strftime('%Y-%m-%d'),maxtime.strftime('%Y-%m-%d')

from commonquery import *
from etlhelper import *

exist_df = getDailyPriceFromDb(code,mintimestr,maxtimestr)    
exist_df['date'] = pd.to_datetime(exist_df['date'])
joincol = ['date','code']
new,exist = filterNewExistTable(df,exist_df,joincol,joincol,'PriceId',False)


pd.read_html('https://finance.naver.com/item/sise_day.nhn?code=000020&page=2',header=0)
page_limit = 3
url = f'http://finance.naver.com/item/sise_day.nhn?code={code}'
new_col_names= {'날짜': 'date', '종가': 'closeprice', '전일비': 'pricediff', '시가': 'openprice', '고가': 'highprice', '저가': 'lowprice', '거래량': 'volume'}    
for page in range(1,page_limit+1):
    pg_url  = f'{url}&page={page}'
    df = df.append(pd.read_html(pg_url,header=0)[0],ignore_index=True)
df = df.rename(columns = new_col_names)
df['date'] = pd.to_datetime(df['date'])
df['code'] = code       
df = df[df.date.notnull()]
df['yeardate'] = df['date'].apply(lambda x : x.year)
df['monthdate'] = df['date'].apply(lambda x: x.month)
return df
except Exception as e:
print(e)
return df


def loadDailyPrice(c:str,pagenum:int=1):
  try:
    print(f'==================== code : {c}  =====================')
    df = getDailyStockValue(c,pagenum)    
    mintime,maxtime =  df.date.min(),df.date.max()
    mintimestr,maxtimestr = mintime.strftime('%Y-%m-%d'),maxtime.strftime('%Y-%m-%d')
    exist_df = getDailyPriceFromDb(c,mintimestr,maxtimestr)    
    exist_df['date'] = pd.to_datetime(exist_df['date'])
    joincol = ['date','code']
    new,exist = filterNewExistTable(df,exist_df,joincol,joincol,'PriceId',False)
    new.to_sql('DailyPrice',sqlserver,'dbo',if_exists='append',index=False)
    print(f'code : {c} => {len(new)} rows inserted')
    print('=========================================================')
  except Exception as e:
    print(e)
  
codes = getCodeInfo().code.unique()
def loadData(pages:int):
  num_cores = multiprocessing.cpu_count()
  codes = getCodeInfo().code.unique()
  parmap.map(loadDailyPrice,codes,pages,pm_pbar=True,pm_processes=num_cores)
