from dbconnector import sqlserver
import pandas as pd

def getCodeInfo(name:str=None):
  try:    
    sql = f"select * from dbo.Code where name = '{name}'" if name != None else 'select * from dbo.Code'
    return pd.read_sql(sql,sqlserver)
  except Exception as e:
    return None

def getEtfCodeInfo(name:str=None):
  try:    
    sql = f"select * from dbo.EtfCode where name = '{name}'" if name != None else 'select * from dbo.EtfCode'
    return pd.read_sql(sql,sqlserver)
  except Exception as e:
    return None

def getDailyPriceFromDb(code:str,fromdate:str,todate:str):
    try:
        sql = f'''
        select * from DailyPrice
        where code = '{code}'
        and date between '{fromdate}' and '{todate}'
        '''
        return pd.read_sql(sql,sqlserver)
    except Exception as e:
        return None
  
  
def getDailyEtfPriceFromDb(code:str,fromdate:str,todate:str):
    try:
        sql = f'''
        select * from DailyEtfPrice
        where code = '{code}'
        and date between '{fromdate}' and '{todate}'
        '''
        return pd.read_sql(sql,sqlserver)
    except Exception as e:
        return None
  