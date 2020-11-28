import pandas as pd
import requests
from bs4 import BeautifulSoup
from dbconnector import sqlserver
from etlhelper import *


def getUpjongList(url:str,istheme:bool =True):
    try:
        res = []
        if istheme:
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
        else:
            cate = requests.get(url)
            b = BeautifulSoup(cate.text,'html.parser')
            upjongtbl =  b.select('#contentarea_left > table')[0]
            anchors = upjongtbl.select('a')
            res.extend(anchors)
        distinct_res = list(set(res))    
        return distinct_res
    except Exception as e:
        return []
    


def getUpjongDetail(url:str,categoryname:str,istheme:bool=False)->pd.DataFrame:
    try:
        baseurl = 'https://finance.naver.com/'
        siseurl = baseurl + url        
        df = pd.read_html(siseurl,encoding='euc-kr')[2]    
        df = df.rename(columns={'테마명':'name'}) if istheme else df.rename(columns={'종목명':'name'})
        df = df[df['name'].notnull()]
        df['categoryname'] = categoryname
        
        df = df[['categoryname','name']]
        df['name'] = df['name'].apply(lambda x : x.replace('*','').strip())
        return df
    except Exception as e:
        print(e)
    


def getMergedUpjongList(acs,category,istheme:bool=False):
    try:
        merged = pd.DataFrame(columns =['categoryname','name'])
        for a in acs:
            categoryname = a.text
            print(f'=====categoryname : {categoryname}=====')
            suburl = a['href']
            resdf = getUpjongDetail(suburl,categoryname,istheme)
            merged = pd.concat([merged,resdf])
        merged['category']=category
        return merged
    except Exception as e:
        print(e)
    

categorysql = 'select * from Category'
categorydetailsql = 'select * from CategoryDetail'

def loadCategory(df):    
    category_exist_df = pd.read_sql(categorysql,sqlserver)
    category_join_cols = ['category','categoryname']
    nu,_ = filterNewExistTable(df,category_exist_df,category_join_cols,category_join_cols,'CategoryId',False)
    nu = nu[['category','categoryname']]
    nu = nu.drop_duplicates()
    nu.to_sql('Category',sqlserver,'dbo',if_exists='append',index=False)


def loadCategoryDetail(df):        
    category_exist_df = pd.read_sql(categorysql,sqlserver)
    category_join_cols = ['category','categoryname']
    _,e = filterNewExistTable(df,category_exist_df,category_join_cols,category_join_cols,'CategoryId',True)
    e = e[['CategoryId','name']]
    
    upjongdetail_exists_df = pd.read_sql(categorydetailsql,sqlserver)
    upjongdetail_join_cols = ['CategoryId','name']
    nd,_ = filterNewExistTable(e,upjongdetail_exists_df,upjongdetail_join_cols,upjongdetail_join_cols,'CategoryDetailId',False)
    nd[['CategoryId','name']].to_sql('CategoryDetail',sqlserver,'dbo',if_exists='append',index=False)




if __name__ == '__main__':
    urls = [('업종별','https://finance.naver.com/sise/sise_group.nhn?type=upjong',False),
            ('테마별','https://finance.naver.com/sise/theme.nhn',True)]

        
    for cate,url,flag in urls:
        print(f'load {cate}')
        anchors = getUpjongList(url,flag)
        resdf = getMergedUpjongList(anchors,cate)
        loadCategory(resdf)
        loadCategoryDetail(resdf)

# a = getUpjongList('https://finance.naver.com/sise/theme.nhn')
# aa= a[1]
# suburl = aa['href']
# baseurl = 'https://finance.naver.com/'
# siseurl = baseurl + suburl        
# df = pd.read_html(siseurl,encoding='euc-kr')[2]    
# df = df[df['종목명'].notnull()]
# df['categoryname'] = categoryname
# df = df.rename(columns={'종목명':'name'})
# df = df[['categoryname','name']]
# df['name'] = df['name'].apply(lambda x : x.replace('*','').strip())
# # import numpy as np
# # d = np.random.randint(1,10,[3,3])
# # d2 = np.random.randint(1,10,[3,3])
# dff = pd.DataFrame(d)
# dff2 = pd.DataFrame(d2)
# pd.concat([dff,dff2])