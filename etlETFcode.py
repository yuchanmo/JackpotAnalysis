import pandas as pd
from dbconnector import sqlserver

df = pd.read_csv(r'D:\Programming\stocktrading\trendanalyzer\etfcode.txt',encoding='utf-8',delimiter='\t')
df.columns = ['StandardCode', 'ShortCode', 'KoreanName', 'KoreanShortName', 'EnglishName', 'ListedDate', 'BasicIndexName',
'IndexCompany', 'TrackingMultiple', 'ReplicationMethod', 'BasicMarketClassification', 'BasicAssetClassification', 'ListedNumber', 'Operator', 'CUQuantity', 'GrossRemuneration', 'Tax Type']
df['ShortCode'] = df['ShortCode'].astype('str')
df['ShortCode'] = df['ShortCode'].apply(lambda x : x if len(x) == 6 else ('0000' + x)[-6:] )

df.to_sql('EtfCode',sqlserver,'dbo',if_exists='replace',index=False)


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
    

def getDailyStockValue(code,page_limit:int = 100):
  df = pd.DataFrame()
  try:
    # url = f'http://finance.naver.com/item/sise_day.nhn?code={code}'
    # new_col_names= {'날짜': 'date', '종가': 'closeprice', '전일비': 'pricediff', '시가': 'openprice', '고가': 'highprice', '저가': 'lowprice', '거래량': 'volume'}    
    # for page in range(1,page_limit+1):
    #   pg_url  = f'{url}&page={page}'
    #   df = df.append(pd.read_html(pg_url,header=0)[0],ignore_index=True)
    # df = df.rename(columns = new_col_names)
    # df['date'] = pd.to_datetime(df['date'])
    # df['code'] = code       
    a = requests.get(f'https://m.stock.naver.com/api/item/getPriceDayList.nhn?code={code}&pageSize={page_limit}&page=1')
    res = json.loads(a.content)
    rows = res['result']['list']
    cols = ['date','closeprice','rf','pricediff','cr','openprice','highprice','lowprice','volume']
    df = pd.DataFrame(rows)
    df.columns = cols
    df = df.drop(columns=['rf','cr'])
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
    exist_df = getDailyEtfPriceFromDb(c,mintimestr,maxtimestr)    
    exist_df['date'] = pd.to_datetime(exist_df['date'])
    joincol = ['date','code']
    new,exist = filterNewExistTable(df,exist_df,joincol,joincol,'EtfPriceId',False)
    new.to_sql('DailyEtfPrice',sqlserver,'dbo',if_exists='append',index=False)
    print(f'code : {c} => {len(new)} rows inserted')
    print('=========================================================')
  except Exception as e:
    print(e)
  

def loadData(pages:int):
  num_cores = multiprocessing.cpu_count()
  codes = getEtfCodeInfo().ShortCode.unique()
  for c in codes:
    loadDailyPrice(c,pages)


loadData(900)

if __name__ =='__main__':  
  pages = 5 if len(sys.argv) < 2  else int(sys.argv[1])
  loadData(pages)
  