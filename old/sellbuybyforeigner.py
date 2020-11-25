import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
##content > div.section.cop_analysis > div.sub_section > table


#https://finance.naver.com/item/frgn.nhn?code=096530
#https://finance.naver.com/item/frgn.nhn?code=096530&page=1

class TableInfo(object):
    def __init__(self,cate,selector,columnnames):
        self.cate = cate
        self.selector = selector
        self.columnnames = columnnames


class CodeInfo(object):
    base_url = 'https://finance.naver.com/item/frgn.nhn?code=<code>&page=1'

    def __init__(self,code,tableinfos):
        url = self.base_url.replace('<code>',code)
        print(url)
        res = requests.get(url)
        html = res.text        
        self.tableinfos = tableinfos
        self.soup = BeautifulSoup(html,'html.parser')
        self.resdict = dict()
        for info in self.tableinfos:
            print(f'===={info.cate}====')
            self.resdict[info.cate] = self._getTableFromHtml(info)
        self._cleansingData()

    def _getTableFromHtml(self,tinfo:TableInfo):
        selector = tinfo.selector
        table = self.soup.select(selector)
        df = pd.read_html(str(table))[0]
        df.columns = tinfo.columnnames
        return df

    def _cleansingData(self):
        reslist = []
        for k in self.resdict.keys():
            if k == '매매동향':
                self.resdict[k] = self.resdict[k].dropna()
            else:
                reslist.append(self.resdict[k])
        self.summary_df = pd.concat(reslist)


buysellinfo = TableInfo('매매동향','#content > div.section.inner_sub > table.type2',['날짜', '종가', '전일비', '등락률', '거래량', '기관_순매매량', '외국인_순매매량', '외국인_보유주수',
       '외국인_보유율'])
codeinfo = TableInfo("종목정보",'#tab_con1 > div.first > table',['Column','Value'])
opinion = TableInfo('투자의견','#tab_con1 > div:nth-child(4) > table',['Column','Value'])
pereps = TableInfo('PEREPS','#tab_con1 > div:nth-child(5) > table',['Column','Value'])
samecate = TableInfo('동일업종PER','#tab_con1 > div:nth-child(6) > table',['Column','Value'])

tableinfolist = [buysellinfo,codeinfo,opinion,pereps,samecate,]
s = CodeInfo('096530',tableinfolist)

s.summary_df

s.resdict
# code = '096530'
# url = 'https://finance.naver.com/item/frgn.nhn?code={code}&page=1'
# res = requests.get(url)
# html = res.text
# soup = BeautifulSoup(html,'html.parser')

# #외국인/기관 매매동향
# buysell_selector = '#content > div.section.inner_sub > table.type2'
# table = soup.select(buysell_selector)
# df = pd.read_html(str(table))[0]
# df.columns = [c[0] if c[0]==c[1] else f'{c[0]}_{c[1]}'  for c in df.columns]
# df = df.dropna()

# #종목정보
# code_info_selector = '#tab_con1 > div.first > table'
# t1 = soup.select(code_info_selector)
# df = pd.read_html(str(t1))[0]

# #투자의견
# selector = '#tab_con1 > div:nth-child(4) > table'
# t2 = soup.select(selector)
# df = pd.read_html(str(t2))[0]

# #PER/EPS
# selector = '#tab_con1 > div:nth-child(5) > table'
# t3 = soup.select(selector)
# df  = pd.read_html(str(t3))[0]

# #동일업종
# #tab_con1 > div:nth-child(6) > table

# selector = '#tab_con1 > div.first > table'

# https://finance.naver.com/item/frgn.nhn?code=096530&page=1
# #content > div.section.inner_sub > table.type2
# df.columns