
import requests
import pandas as pd
import json
import math
from dbconnector import sqlserver
import pymysql
from sqlalchemy import create_engine
from datetime import datetime
from etlhelper import *


class PriceAfterWorkingHours(object):
    header = {
    'Host': 'finance.daum.net',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://finance.daum.net/domestic/after_hours',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': '_TI_NID=iok9mjEFfnWoNqMjDA5hhUz8RnRoFJmjeMkjFvT7JYdrJYTW75KEha6AtdEFb1tIzandH1pdBhNpEJoajFst7Q==; _ga=GA1.2.907775595.1596724382; TIARA=vnh3X-3kihrfw214TyVI6JlrkHYWmUEBBkDF8n7YhIodUJ5AJeF6ldbXDYcfAzo2IRlktZNC5LhK77yMQeXPkdwVbjdWgbDb; __T_=1; _gid=GA1.2.946178065.1598876628; _dfs=Y2FJRmFFaVJHM3Y5TDJPMUhpeFFVRkoxNkJ5RmJ6ZU1QTXc4Y2FNSkJ4UGJ1RDVNbVk4dWptTEJMb05xSTNpa0VBOEdTOHZwN3BOWnZJZ1ZzbTdFa3c9PS0tdU1uUGg1eDRyLzZkcG1TbHhlYmkxQT09--1f18d56bc949623459ad90a1fe5f9896f2054874',
    }
    per_count = 30
    base_url = f'http://finance.daum.net/api/trend/after_hours_spac?page=<pagenum>&perPage=<perpagenum>&fieldName=changeRate&order=desc&market=<category>&type=CHANGE_RISE&pagination=true'
    
    def __init__(self):
        datalist = [self.initializeData(c) for c in  ['KOSPI','KOSDAQ']]
        self.resdf = pd.concat(datalist)
        
    def initializeData(self,cate):
        print(f'========load {cate} data=========')
        check_url = self.getUrlForData(cate)
        data_for_check = self.getDataFromUrl(check_url)
        self.totalPages, self.totalCount,self.baseDate = data_for_check['totalPages'],data_for_check['totalCount'],data_for_check['baseDate']        
        iter_limit = math.ceil(self.totalCount/self.per_count)+1
        reslist=[]
        for i in range(1,iter_limit):
            try:
                data_url = self.getUrlForData(cate,i,self.per_count)
                print(f'load data from {(i-1)*self.per_count} to {(i)*self.per_count}')
                tmpdata = self.getDataFromUrl(data_url)['data']
                reslist.extend(tmpdata)        
            except Exception as e:
                print(e)
                pass            
        df = pd.DataFrame(reslist)
        df['date'] = self.baseDate    
        df['cate'] = cate
        return df
    
    @classmethod
    def getUrlForData(cls,category='KOSPI', pagenum=1,perpagenum=1):        
        url_for_data = cls.base_url.replace('<category>',category).replace('<pagenum>',str(pagenum)).replace('<perpagenum>',str(perpagenum))
        return url_for_data

    @classmethod
    def getDataFromUrl(cls,url:str):            
        res = requests.get(url,headers= cls.header)        
        html = res.text        
        resdict = json.loads(html)        
        return resdict

def loadPriceAfterWokringHour():
    p =PriceAfterWorkingHours()
    p.resdf = p.resdf.rename(columns={'change':'change','code':'fullcode'})
    p.resdf['code'] = p.resdf['symbolCode'].str[1:]
    p.resdf['Regdate'] = datetime.today().strftime('%Y-%m-%d')
    cols = list(p.resdf)
    p.resdf['date'] = pd.to_datetime(p.resdf['date'])
    join_cols = ['date', 'cate', 'rank', 'name', 'symbolCode', 'code', 'tradePrice', 'change', 'changePrice', 'changeRate', 'pricePerformance', 'accTradeVolume', 'accTradePrice', 'regularHoursTradePrice', 'regularHoursChange', 'regularHoursChangePrice', 'regularHoursChangeRate']
    filterdate = p.resdf['date'].iloc[0].strftime('%Y-%m-%d')
    print(f'query from db for date {filterdate}')
    dbdf = pd.read_sql(f"select * from PriceAfterWorkingHour where date='{filterdate}'",sqlserver)
    dbdf['date'] = pd.to_datetime(dbdf['date'])
    print('join data')
    n,_ = filterNewExistTable(p.resdf,dbdf,join_cols,join_cols,'PriceAfterHourId')    
    print('insert new data')    
    n[cols].to_sql('PriceAfterWorkingHour',sqlserver,if_exists='append',index=False)
    print(f'total {len(rdf)} rows inserted')

if __name__ =='__main__':
    loadPriceAfterWokringHour()
