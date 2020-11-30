import parmap
import multiprocessing
#import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import datetime
from scipy.signal import argrelextrema
import pandas as pd 
import numpy as np
from dbconnector import sqlserver
from sklearn.preprocessing import MinMaxScaler,PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error,r2_score
from etlhelper import *
import sys

def minusSlope(df,start:str=None,end:str=None):
      reslist = []
      for t in ['3avg','5avg']:
        data = df[start:end][t] if (start ==None) and (end == None) else df
        y = data.values      
        x = np.arange(len(y)).reshape(-1,1)
        model = LinearRegression()
        model.fit(x,y)
        reslist.append(model.coef_)
      reslistarr = np.array(reslist)
      #print(reslistarr) 
      return np.all(reslistarr<0)


def getBestFitModel(df,start:str=None,end:str=None,showplot:bool = False):
      '''
      return 상승중인지?, Fit Score, 가장 잘맞는 Degree는??(1~3차중),Coef
      '''
      data= df[start:end]['close'] if (start ==None) and (end == None) else df      
      y = data.values      
      x = np.arange(len(y))
      score = 0 
      bestdegree = 0
      coef = 0
      
      for i,degree in enumerate([1,2]):
            xx = x.reshape(-1,1)
            yy = y.reshape(-1,1)
            model = make_pipeline(PolynomialFeatures(degree),LinearRegression())
            model.fit(xx,yy)
            py = model.predict(xx).flatten()              
            tcoef = model[1].coef_
            tscore = model.score(xx,yy)
            # print('last coef : ',tcoef[-1],'/ is positive??',tcoef[0][-1]>0)
            # print('model score',tscore)
            if tscore >= score:
                  bestdegree = degree
                  score = tscore
                  coef = tcoef
      
      ascending = coef[0][-1]>0
      return ascending,score,bestdegree,coef



class DailyStockValue():  
  def __init__(self,df:pd.DataFrame):
      try:                
        self.code = df['code'].unique()[0]
        self.name = df['name'].unique()[0]
        self.df = df[['date','close', 'price', 'open', 'high', 'low', 'volume']]        
        self.calculateDataFrame()
      except Exception as e:
        print('없는 종목입니다')
        pass
  
  def calculateDataFrame(self):      
      df = self.df
      df['date'] = pd.to_datetime(df['date'])
      df = df.set_index('date')
      df = df[df['close'].notnull()]
      df = df.sort_index()   
      #self.lastdate = df.iloc[-1]['date']

      #증감
      diffportion = round(df/df.shift(1)-1,3)*100
      diffportion = diffportion.add_suffix('_diffportion')
      #add rolling (이동평균선)
      rollingdays = [(3,3),(5,3),(20,10),(60,30),(120,20)]
      for r,rm in rollingdays:
        colname = str(r)+'avg'
        df[colname]=df['close'].rolling(r,min_periods=rm).mean()        
      #지지선 : minpoint / 저항선 : maxpoint
      df = pd.concat([df,diffportion],axis=1)        
      df['minpoint'] = df.iloc[argrelextrema(df.close.values,np.less_equal)]['close']
      df['maxpoint'] = df.iloc[argrelextrema(df.close.values,np.greater_equal)]['close']
      df['close3avg'] = df['close']/df['3avg']
      df['open_close'] = df['close']-df['open']
      df['open_close_diffportion'] = df['open_close']/df['open']*100
      self.df = df
      self.lastdate = df.index[-1].strftime('%Y-%m-%d')
  
  def getAvgMinMaxOfCloseValueBetweenStartAndEnd(self,start,end):
      df = self.df
      filtered_df = df[start:end]['close']
      return filtered_df.mean(),filtered_df.min(),filtered_df.max() 

  def getCloseValue(self,date):
      return self.df[date]['close']

  def __repr__(self):
      return f'{self.code}_{self.name}'

  def revertTrend(self):
      recent_data = self.df[-10:]      
      today_data = self.df.iloc[-1]      
      yesterday_data = self.df.iloc[-2]      
      is_minus_slope = minusSlope(recent_data)
      open_close_diff = today_data['open_close_diffportion']
      volum_diff_portion = today_data['volume_diffportion']
      avg_diff_between_y_t = abs((today_data['3avg'] - yesterday_data['3avg'])/today_data['3avg'])*100
      return is_minus_slope and \
             open_close_diff >2.0 and avg_diff_between_y_t<1.5 

  #장대양봉
  #지난5일이상을 덮어버리는 양봉
  def longCandle(self):      
      recent_data = self.df[-6:-1]      
      today_data = self.df.iloc[-1]            
      is_minus_slope = minusSlope(recent_data)
      recent_max = recent_data['high'].max()
      today_close = today_data['close']      
      volume_diff_portion = today_data['volume_diffportion']      
      return is_minus_slope and  today_close > recent_max and volume_diff_portion > 200                        

  def lowVolumnMeetAvg3(self):
      recent10days = self.df[-10:]
      recent3days = self.df[-3:]
      days10ascending, score, degree,_ = getBestFitModel(recent10days)
      days3ascending,score,degree,_ = getBestFitModel(recent3days)
      threedaysago =recent10days.iloc[-3]
      twodaysago = recent10days.iloc[-2]
      yesterday = recent10days.iloc[-1]
      predicate = ((float(twodaysago.volume_diffportion)>100.0) and \
                  (float(yesterday.volume_diffportion) <-50.0) and \
                  (float(yesterday.close3avg) <= 1.1) and \
                  (float(twodaysago.close_diffportion)>5) and \
                  (float(yesterday.close_diffportion)>0)) or\
                  ((float(threedaysago.volume_diffportion)>100.0) and \
                  (float(twodaysago.volume_diffportion) <-50.0) and \
                  (float(yesterday.volume_diffportion) <0.0) and \
                  (float(yesterday.close3avg <= 1.1))) and \
                  (float(threedaysago.close_diffportion)>5) and \
                  (float(twodaysago.close_diffportion)>-1) and \
                  (float(yesterday.close_diffportion)>-1) and\
                  (days10ascending) and (days3ascending)
      return predicate


def extractKeyItemsFromStockValue(fromdate:str)->list:    
    s = f'''
    select c.name	   
        ,c.code as [code]
        ,[date]
        ,[closeprice] as [close]
        ,[pricediff] as [price]
        ,[openprice] as [open]
        ,[highprice] as [high]
        ,[lowprice] as [low]
        ,[volume] as [volume]
    from DailyPrice d
    join Code c
        on d.code = c.code
    where  [date] between dateadd(d,-20,'{fromdate}') and '{fromdate}'
    '''

    restuple =[]
    dd = pd.read_sql(s,sqlserver)
    resdate = dd['date'].max().strftime('%Y-%m-%d')
    for gn,g in dd.groupby(['name']):
        try:
            print(f'table name : {gn}')    
            stockval = DailyStockValue(g)        
            if stockval.lowVolumnMeetAvg3():
                print('added new 폭등 data :',stockval.name)
                restuple.append((resdate,'폭등',stockval.code))
            if stockval.revertTrend():
                print('added new 반전 data :',stockval.name)
                restuple.append((resdate,'반전',stockval.code))
            if stockval.longCandle():
                print('added new 장대 data :',stockval.name)
                restuple.append((resdate,'장대',stockval.code))
        except Exception as e:
            pass
    resdf = pd.DataFrame(columns=['issuedate','category','code'],data=restuple)
    return resdf

def loadKeyItem(fromdate:str):
    try:
        fromdate = fromdate if fromdate is not None else datetime.datetime.today().strftime('%Y-%m-%d')
        resdf = extractKeyItemsFromStockValue(fromdate)
        exist_df = pd.read_sql(f"select * from KeyItem where issuedate = '{fromdate}'",sqlserver)    
        resdf['issuedate'] = pd.to_datetime(resdf['issuedate'])
        exist_df['issuedate'] = pd.to_datetime(exist_df['issuedate'])
        join_cols = ['issuedate','category','code']
        n,_ = filterNewExistTable(resdf,exist_df,join_cols,join_cols,'KeyItemId')
        resdf.to_sql('KeyItem',sqlserver,'dbo',if_exists='append',index=False)
        print(f'total {len(n)} rows inserted')
    except Exception as e:
        print(e)
    


if __name__ == '__main__':
    arglen = len(sys.argv)
    if arglen == 1:
        print('load for today date')
        extractdate = None
        loadKeyItem(extractdate)
    elif arglen == 2:        
        extractdate = sys.argv[1]
        print(f'load for {extractdate}')
        loadKeyItem(extractdate)
    elif arglen == 3:        
        daterange = [d.strftime('%Y-%m-%d') for d in pd.date_range(sys.argv[1],sys.argv[2])]
        print(f'load for {daterange}')
        for extractdate in daterange:
            loadKeyItem(extractdate)

# tmp = pd.DataFrame(columns = ['issuedate','category','code'], data=[('2020-11-27','반전','001210')])
# tmp.info()
# exist_df.info()
# exist_df = pd.read_sql(f"select * from KeyItem where issuedate = '2020-11-27'",sqlserver)    
# tt = exist_df[exist_df['code'] == '001210']
# tmp['issuedate'] = pd.to_datetime(tmp['issuedate'])
# tt['issuedate'] = pd.to_datetime(tt['issuedate'])
# join_cols = ['issuedate','category','code']
# pd.merge(tmp,tt,left_on=join_cols,right_on=join_cols)
# colforexist = 
# merged = pd.merge(tmp,tt,left_on=join_cols,right_on=join_cols,how='left',suffixes=['','_y'])
# colkey = colforexist+'_y' if colforexist + '_y' in list(merged) else colforexist
# new,exist = merged[merged[colkey].isnull()],merged[merged[colkey].notnull()]  
# leftcols = list(left)
# if containsright:
#     return new,exist  
# else:
#     return new[leftcols],exist[leftcols]

# n,_ = filterNewExistTable(tmp,tt,join_cols,join_cols,'KeyItemId')

# df['date'] = pd.to_datetime(df['date'])
# df = df.set_index('date')
# df = df[df['close'].notnull()]
# df = df.sort_index()   
# df['code'].unique()[0]
# df['name'].unique()[0]
# df = df[['close', 'price', 'open', 'high', 'low', 'volume']]
# diffportion = round(df/df.shift(1)-1,3)*100
# diffportion = diffportion.add_suffix('_diffportion')
