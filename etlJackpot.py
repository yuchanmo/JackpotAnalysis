from scipy.signal import argrelextrema
import pandas as pd
from dbconnector import sqlserver
from datetime import datetime
import matplotlib.pyplot as plt
from etlhelper import *
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


print('start to find jackpot item')
# sql = '''
# select c.name,p.code,p.curval,p.curvol,p.Regdate
#   from Stock.dbo.AllTimePriceFromNaver p
#   join code c
# 	on p.code = c.code
#   where Regdate >= DATEADD(MINUTE,-10,getdate())
# '''

def loadData():  
  try:
    fromstr = datetime.today().strftime('%Y-%m-%d')
    #fromstr = '2020-12-14'

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
    return df
  except Exception as e:
    print(e)
  

def findInflectionPoint(valarr):
    f_prime = np.gradient(valarr) # differential approximation
    indices = np.where (np.diff (np.sign(f_prime))) [0] # Find the inflection point.
    return indices


def calculateStats(g:pd.DataFrame):    
    g = g.sort_index()
    rollingdays = [(3,1),(7,1)] #3avg/7avg
    for r,rm in rollingdays:
        colname = 'avg'+str(r)
        g[colname]=g['curval'].rolling(r,min_periods=rm).mean()  
    val = g[['curval','curvol','avg3','avg7']]
    valdiff1 = round(val/val.shift(1)-1,3)*100 #직전 거래 차이
    valdiff1 = valdiff1.add_suffix('_1diff')
    valdiff3 = round(val/val.shift(3)-1,3)*100 #2개전 거래 차이
    valdiff3 = valdiff3.add_suffix('_3diff')   
    # idx_val_infle = findInflectionPoint(g['curval']) #변곡점 찾기
    # idx_vol_infle = findInflectionPoint(g['curvol'])    
    # real_idx_val_infle = g.iloc[idx_val_infle].index
    # real_idx_vol_infle = g.iloc[idx_val_infle].index
    g['val_infle']=0
    g['vol_infle']=0
    # g.at[real_idx_val_infle,'val_infle']=1
    # g.at[real_idx_vol_infle,'vol_infle']=1
    g['startvol_curvol_diff']=round((g['curvol']-g['startvol'])/g['startvol'] * 100,2)
    g['startval_curval_diff']=round((g['curval']-g['startval'])/g['startval'] * 100,2)
    return pd.concat([g,valdiff1,valdiff3,],axis=1)

def recent2Maxim2Minimum(g):
  x = g['curval'].values
  maxx = argrelextrema(x, np.greater)[0]
  minn = argrelextrema(x, np.less)[0]
  mm = g.iloc[minn]['curval'][-1:].values
  mm = mm[0] if len(mm)>0 else 0
  mx = g.iloc[maxx]['curval'][-1:].values
  mx = mx[0] if len(mx)>0 else 0
  return mm,mx

def loadExistData():
  sql ='''
  SELECT JackpotId
      ,[Regdate]
      ,[cate]
      ,[code]      
  FROM [Stock].[dbo].[Jackpot]
  where Regdate >= dateadd(hour,-50,getdate())
  '''
  return pd.read_sql(sql,sqlserver)

def fitAndFindRevert(rows):
  y = rows['curval'].values
  x = np.arange(0,len(y))
  X = x.reshape(-1,1)
  res = []
  for degree in range(1,5):    
      polyreg=make_pipeline(PolynomialFeatures(degree),LinearRegression())
      polyreg.fit(X,y)
      d = degree
      c = polyreg[1].coef_
      res.append(c[-1])
  return (res[0]>0) and (res[1]<0) and (res[2]>0) and (res[3]>0)
  
# s = df[df['name']=='현대바이오']
# len(s)
# for i in range(0,870):
#   st = 0 if i<=10 else i-10
#   en = 1 if i==0  else i    
#   res = fitAndFindRevert(s.iloc[st:en])
#   if res:
#     print(s.iloc[en])

init_df = loadData()
df = init_df.groupby(['code']).apply(calculateStats)
cols = list(df)
cols.remove('code')
df = df[cols]
df = df.reset_index(level=0)
last3df = df.groupby(['code']).apply(lambda x : x[-3:][cols]).reset_index(level=[0])


cond1 = (last3df['curval_1diff']>0.3) & (last3df['curval_3diff']>0.8) #& (last3df['curvol_1diff']>20) & (last3df['curvol_3diff']>50) #꿈틀??
cond2 = (last3df['curval_1diff']>0.5) & (last3df['curval_3diff']>1.2) #& (last3df['curvol_3diff']>30) #꾸준한놈
conds = [('꿈틀',cond1),('더꿈틀',cond2),]

datalist = []
for cn,c in conds:
    itemlist = last3df[c]
    current = itemlist.groupby(['code']).apply(lambda x : x[-1:][cols]).reset_index(level=[0]).reset_index()
    current['cate'] = cn    
    datalist.append(current)
    
issuedf = pd.concat(datalist)
min_max_df = df.groupby(['code']).apply(recent2Maxim2Minimum).apply(pd.Series).reset_index()
min_max_df.columns = ['code','low','high']
revert_df = df.groupby(['code']).apply(lambda x : fitAndFindRevert(x[-10:][['curval']])).reset_index(level=0)
revert_df.columns = ['code','revert_trend']

final_df= pd.merge(issuedf,min_max_df,left_on=['code'],right_on=['code'],how='left')
final_df= pd.merge(final_df,revert_df,left_on=['code'],right_on=['code'],how='left')
final_df_cols = ['Regdate','cate', 'code', 'name', 'startval', 'startvol','curval', 'curvol','startvol_curvol_diff', 'startval_curval_diff',  'avg3', 'avg7', 'val_infle', 'vol_infle', 'curval_1diff', 'curvol_1diff', 'avg3_1diff', 'avg7_1diff', 'curval_3diff', 'curvol_3diff', 'avg3_3diff', 'avg7_3diff', 'low','high','revert_trend']
fdf = final_df[final_df_cols]
fdf.replace(np.inf,0,inplace=True)
fdf.head()
if len(fdf)>0:
  joincols = ['Regdate','code','cate']
  exist_df = loadExistData()
  n,e = filterNewExistTable(fdf,exist_df,joincols,joincols,'JackpotId')
  n.to_sql('Jackpot',sqlserver,'dbo',if_exists='append',index=False)
  print(f'{len(n)} rows inserted')

    
