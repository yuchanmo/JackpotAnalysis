from dbconnector import sqlserver,mysql
import pandas as pd

def getCodeInfo(name:str=None):
  try:    
    sql = f"select * from Code where name = '{name}'" if name != None else 'select * from Code'
    return pd.read_sql(sql,mysql)
  except Exception as e:
    return None

def getEtfCodeInfo(name:str=None):
  try:    
    sql = f"select * from EtfCode where name = '{name}'" if name != None else 'select * from EtfCode'
    return pd.read_sql(sql,mysql)
  except Exception as e:
    return None

def getDailyPriceFromDb(code:str,fromdate:str,todate:str):
    try:
        sql = f'''
        select * from DailyPrice
        where code = '{code}'
        and date between '{fromdate}' and '{todate}'
        '''
        return pd.read_sql(sql,mysql)
    except Exception as e:
        return None
  
  
def getDailyEtfPriceFromDb(code:str,fromdate:str,todate:str):
    try:
        sql = f'''
        select * from DailyEtfPrice
        where code = '{code}'
        and date between '{fromdate}' and '{todate}'
        '''
        return pd.read_sql(sql,mysql)
    except Exception as e:
        return None
  