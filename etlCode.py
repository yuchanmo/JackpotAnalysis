import pandas as pd
from dbconnector import sqlserver,mysql
from etlhelper import filterNewExistTable

#def loadCode():
code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0] 
# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌 
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
cols = ['회사명','종목코드','업종','주요제품','상장일','결산월']
code_df = code_df[cols]
# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다. 
# 한글로된 컬럼명을 영어로 바꿔준다. 
colname_map = {'회사명':'name','종목코드':'code','업종':'category','주요제품':'products','상장일':'issuedate','결산월':'settlementdate'}
code_df = code_df.rename(columns=colname_map)   

exist_df = pd.read_sql('select * from Code',mysql)
joincols = ['code']
#code_df.to_sql('Code',mysql,if_exists='append',index=False)

n,e = filterNewExistTable(code_df,exist_df,joincols,joincols,'Id',False)
n.to_sql('Code',sqlserver,if_exists='append',index=False)
print(f'{len(n)} rows inserted')