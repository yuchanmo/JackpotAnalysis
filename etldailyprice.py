from dbconnector import sqlserver,mysql
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
    # exist_df = getDailyPriceFromDb(c,mintimestr,maxtimestr)    
    # exist_df['date'] = pd.to_datetime(exist_df['date'])
    # joincol = ['date','code']
    # new,exist = filterNewExistTable(df,exist_df,joincol,joincol,'code_y',False)
    df.to_sql('DailyPrice',mysql,if_exists='append',index=False)
    print(f'code : {c} => {len(df)} rows inserted')
    print('=========================================================')
  except Exception as e:
    print(e)
  

def loadData(pages:int):
  num_cores = multiprocessing.cpu_count()
  codes = getCodeInfo().code.unique()
  for c in codes:
    loadDailyPrice(c,pages)

  #parmap.map(loadDailyPrice,codes,pages,pm_pbar=True,pm_processes=num_cores)


if __name__ =='__main__':  
  pages = 5 if len(sys.argv) < 2  else int(sys.argv[1])
  loadData(pages)
  

# from datetime import datetime
# d = datetime(2020,1,1)
# d.month
# d.year

# for c in codes:
#   item = getDailyStockValue('DSR',1)

#   item.resdf
  
#   item.resdf
# t = getCodeInfo()
# u = 'http://finance.naver.com/item/sise_day.nhn?code=155660'
# df = pd.read_html(u,header=0)

