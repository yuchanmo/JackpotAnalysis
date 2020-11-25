# 시총, 증가율(YOY/QOQ/실적), 목표주가(계산), Naver 증권가 목표주가, 코로나 이전(2020년 1~3월대비) 현재 주가

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
##content > div.section.cop_analysis > div.sub_section > table


def initializeCodeDf():
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0] 
    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌 
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
    cols = ['회사명','종목코드','업종','주요제품','상장일','결산월']
    code_df = code_df[cols]
    # 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다. 
    # 한글로된 컬럼명을 영어로 바꿔준다. 
    colname_map = {'회사명':'name','종목코드':'code','업종':'category','주요제품':'products','상장일':'issuedate','결산월':'settlementdate'}
    code_df = code_df.rename(columns=colname_map)   
    return code_df


def addsuffixForDataFrame(data:pd.DataFrame, suffix:str):
    cols = data.columns
    data.columns = pd.MultiIndex.from_tuples([(a,f'{b}_{suffix}') for a,b in cols])
    return data

def addsuffix(cols:pd.core.indexes.multi.MultiIndex, suffix:str):
    return pd.MultiIndex.from_tuples([(a,f'{b}_{suffix}') for a,b in cols])

def filterNull(data:pd.DataFrame):
    filter_cond = data.isnull().all()
    filter_cond_index = filter_cond[filter_cond == False].index
    return data[filter_cond_index]

def addSuffixAndFilterNull(data:pd.DataFrame,suffix:str):
    data = addsuffixForDataFrame(data,suffix)
    return filterNull(data)



def summarizeAsset(row):
    try:
        code = row['code']
        name = row['name']
        category = row['category']
        products = row['products']
        print(f'summarize {code}_{name}')
        url = f'https://finance.naver.com/item/main.nhn?code={code}'
        res = requests.get(url)
        html = res.text
        soup = BeautifulSoup(html,'html.parser')
        asset_selector = 'div.sub_section > table'
        table = soup.select(asset_selector)
        volumn_df,close_df,asset_df = pd.read_html(str(table))
        summary = pd.concat([asset_df.xs('주요재무정보',level=0,axis=1),  asset_df.xs('최근 분기 실적',level=0,axis=1)],axis=1)
        summary.columns = summary.columns.droplevel(level=1)
        summary = summary.set_index('주요재무정보',drop=True)
        yearmonth = [(c.split('.')[0],c.split('.')[1][:2]) for c in summary.columns]
        summary.columns = pd.MultiIndex.from_tuples(yearmonth)
        summary = summary.replace('-',0).apply(lambda x : x.astype('float'))
        # percent
        #swap_summary = summary.swapaxes('index','columns')
        yoy_pct = summary.groupby(axis=1,level=1).pct_change(axis='columns') * 100
        yoy_pct = addSuffixAndFilterNull(yoy_pct,'_yoy_pct')
        yoy_diff = summary.groupby(axis=1,level=1).diff(axis='columns')
        yoy_diff = addSuffixAndFilterNull(yoy_diff,'_yoy_diff')
        qoq_pct = summary.pct_change(axis='columns')*100
        qoq_pct = addSuffixAndFilterNull(qoq_pct,'_qoq_pct')
        qoq_diff = summary.diff(axis='columns')
        qoq_diff = addSuffixAndFilterNull(qoq_diff,'_qoq_diff')
        merged = pd.concat([summary,yoy_pct,yoy_diff,qoq_pct,qoq_diff],axis=1)
        merged = merged[sorted(merged.columns.values,key=lambda x : x[0]+x[1])]
        filter_merged = merged.loc[['매출액','영업이익','당기순이익']]
        filter_merged.columns = filter_merged.columns.map('.'.join).str.strip()
        filter_merged = filter_merged.unstack()
        filter_merged = filter_merged.to_frame().T
        filter_merged['NAME']=name
        filter_merged['CODE']=code
        filter_merged['CATEGORY'] = category
        filter_merged['PRODUCTS'] = products
        cols = list(filter_merged)
        return filter_merged[cols[-4:]+cols[:-4]]
    except Exception as e:
        pass
    

code_df = initializeCodeDf()

reslist = []
for i,row in code_df.iterrows():    
    test = summarizeAsset(row)
    reslist.append(test)
    


finalres = pd.concat(reslist)
cocols = list(finalres)
finalres[cocols[-4:]+cocols[:-4]].to_csv('assetres.csv')

.to_csv('result.csv')
