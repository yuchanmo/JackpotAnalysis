import pandas as pd
import requests
from bs4 import BeautifulSoup
from dbconnector import sqlserver
from etlhelper import *

getThemeList()

res = []
for i in range(1,11):
    try:
        cate = requests.get(f'https://finance.naver.com/sise/theme.nhn?&page={i}')
        b = BeautifulSoup(cate.text,'html.parser')
        themetbl =  b.select('#contentarea_left > table.type_1.theme')[0]
        anchors = themetbl.select('a')
        res.extend(anchors)
    except Exception as e:
        print(f'no more page over {i} page')
        break
len(res)

return anchors


def getThemeList():
    cate = requests.get('https://finance.naver.com/sise/theme.nhn')
    b = BeautifulSoup(cate.text,'html.parser')
    themetbl =  b.select('#contentarea_left > table.type_1.theme')[0]
    anchors = themetbl.select('a')
    return anchors


def getThemeDetail(url:str,upjongname:str)->pd.DataFrame:
    baseurl = 'https://finance.naver.com/'
    siseurl = baseurl + url        
    df = pd.read_html(siseurl,encoding='euc-kr')[2]    
    df = df[df['종목명'].notnull()]
    df['themename'] = upjongname
    df = df.rename(columns={'종목명':'name'})
    df = df[['themename','name']]
    df['name'] = df['name'].apply(lambda x : x.replace('*','').strip())
    return df


def getMergedUpjongList(acs):
    merged = pd.DataFrame(columns =['themename','name'])
    for a in acs:
        upjongname = a.text
        print(f'=====themename : {upjongname}=====')
        suburl = a['href']
        resdf = getUpjongDetail(suburl,upjongname)
        merged = pd.concat([merged,resdf])
    return merged

def loadUpjong(df):
    upjongsql = 'select * from Theme'
    upjong_exist_df = pd.read_sql(upjongsql,sqlserver)
    upjong_join_cols = ['upjongname']
    nu,_ = filterNewExistTable(df,upjong_exist_df,upjong_join_cols,upjong_join_cols,'UpjongId',False)
    nu = nu[['upjongname']]
    nu = nu.drop_duplicates()
    nu.to_sql('Upjong',sqlserver,'dbo',if_exists='append',index=False)


def loadUpjongDetail(df):    
    upjong_exist_df = pd.read_sql(upjongsql,sqlserver)
    upjong_join_cols = ['upjongname']
    _,e = filterNewExistTable(df,upjong_exist_df,upjong_join_cols,upjong_join_cols,'UpjongId',True)
    e = e[['UpjongId','name']]
    upjongdetailsql = 'select * from UpjongDetail'
    upjongdetail_exists_df = pd.read_sql(upjongdetailsql,sqlserver)
    upjongdetail_join_cols = ['UpjongId','name']
    nd,_ = filterNewExistTable(e,upjongdetail_exists_df,upjongdetail_join_cols,upjongdetail_join_cols,'UpjongDetailId',False)
    nd[['UpjongId','name']].to_sql('UpjongDetail',sqlserver,'dbo',if_exists='append',index=False)




#if __name__ == '__main__':
anchors = getUpjongList()
resdf = getMergedUpjongList(anchors)
loadUpjong(resdf)
loadUpjongDetail(resdf)




# import numpy as np
# d = np.random.randint(1,10,[3,3])
# d2 = np.random.randint(1,10,[3,3])
# dff = pd.DataFrame(d)
# dff2 = pd.DataFrame(d2)
# pd.concat([dff,dff2])