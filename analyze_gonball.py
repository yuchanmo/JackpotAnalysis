f = open(r'D:\Programming\stocktrading\trendanalyzer\dragonball.txt',encoding='utf-8')
        
start = '[Web발신]'
end = '[핀업 스탁 My 멘토 알리미]'
lines = f.readlines()
flag = False
c = 0
res = []
for l in lines:
    if start in l:
        flag = True
        c = 0
        continue
    if end in l:
        tmp = [name,start_end,buy_price,target_price,loss_price]
        print(tmp)
        res.append(tmp)
        flag = False
        continue
    if flag:
        if c ==0 :
            name = l
        elif c==1:
            pass
        elif c==2:
            start_end = l
        elif c==3:
            buy_price = l
        elif c==4:
            target_price = l
        elif c==5:
            loss_price = l
        else:
            pass
        c+=1
    
    

import pandas as pd
from pandas._libs.missing import NAType
parsed_res = []
for s in res:
    cate = '목표' if '목표' in s[0] else '종료'
    name = s[0].replace('\n','').split(']')[1].strip()
    s_e = s[1].replace('\n','').split('/')
    start_date = s_e[0].strip().split(' ')[1]
    end_date = s_e[1].strip().split(' ')[1]
    p_r = s[2].replace('\n','').split('~')
    start_price = p_r[0].strip().split(' ')[1].replace(',','')
    end_price = p_r[1].strip().split(' ')[0].replace(',','')
    target_price = s[3].split(' ')[1].strip()
    loss_price = s[4].split(' ')[1].strip()
    t = [cate,name,start_date,end_date,start_price,end_price,target_price,loss_price]
    parsed_res.append(t)

df = pd.DataFrame(parsed_res,columns=['분류','name','추천일','목표일','매수저점','매수고점','목표가','손절가'])
df = df.drop_duplicates()
df= df[df['분류']=='목표']
df.to_csv('gon.csv')

from pykrx import stock

markets =['KOSPI','KOSDAQ']
res = []
for m in markets:
  market_ticker = [(m,t,stock.get_market_ticker_name(t),1) for t in stock.get_market_ticker_list(market=m)]
  index_ticker = [(m,t,stock.get_index_ticker_name(t),0) for t in stock.get_index_ticker_list(market=m)]
  res.extend(market_ticker)
  res.extend(index_ticker)



code_df = pd.DataFrame(res,columns=['cate','ticker','name','ismarket'])
code_df = code_df.drop_duplicates()
#code_df.head()
merged_df = pd.merge(df,code_df,left_on=['name'],right_on=['name'],how='inner')
merged_df[['추천일','목표일']] = merged_df[['추천일','목표일']].apply(lambda x : x.replace('-',''))
merged_df.dtypes

code_summary = merged_df[['name','ticker','추천일','목표가']].drop_duplicates().sort_values(by=['추천일'])
code_summary['추천일'] = code_summary['추천일'].apply(lambda x : x.replace('-',''))
rows = []
for i,row in code_summary.iterrows():
    print(row)
    n,t,d,tp = row
    tmp = stock.get_market_fundamental_by_date(d, d, t)
    tmp = tmp.reset_index()
    tmp['ticker'] = t
    rows.append(tmp)
perdf = pd.concat(rows)


merged_df[:3]
price_df = stock.get_market_ohlcv_by_date("20201127", "20210729", "039290")
tmp_df = price_df[price_df['고가']>1118860].reset_index()
tmp_df['날짜'].min()

end_date_list =[]
for i,row in code_summary.iterrows():
    print(row)
    n,t,d,tp = row
    price_df = stock.get_market_ohlcv_by_date(d, "20210729", t)
    tmp_df = price_df[price_df['고가']>float(tp)].reset_index()
    tmp_enddate = tmp_df['날짜'].min()
    #tmp_enddate = tmp_enddate.strftime('%Y%m%d') if tmp_enddate!=pd._libs.tslibs.nattype.NaTType else ''
    end_date_list.append([n,t,d,tmp_enddate])
end_date_df = pd.DataFrame(end_date_list,columns=['name','ticker','startdate','finishdate'])
merged_df['startdate']= pd.to_datetime(merged_df['추천일'])
end_date_df['startdate']= pd.to_datetime(end_date_df['startdate'])
merged_df = pd.merge(merged_df,end_date_df,left_on=['ticker','startdate'],right_on=['ticker','startdate'],how='left')


type(end_date_df.iloc[0][3]) == pd._libs.tslibs.nattype.NaTType
end_rows = []
for i,row in end_date_df.iterrows():
    print(row)
    n,t,d,fd = row
    if type(fd) != pd._libs.tslibs.nattype.NaTType:
        fd = fd.strftime('%Y%m%d')
        tmp = stock.get_market_fundamental_by_date(fd, fd, t)
        tmp = tmp.reset_index()
        tmp['ticker'] = t
        end_rows.append(tmp)
finised_perdf = pd.concat(end_rows)
finised_perdf.columns = ['종료일_'+fp for fp in finised_perdf.columns]
perdf.columns = ['시작일_'+fp for fp in perdf.columns]
m1 = pd.merge(merged_df,perdf,left_on=['ticker','startdate'],right_on=['시작일_ticker','시작일_날짜'],how='left')
m2 = pd.merge(m1,finised_perdf,left_on=['ticker','finishdate'],right_on=['종료일_ticker','종료일_날짜'],how='left')
m2.to_csv('gongon.csv')

sichong =[]
m2.columns
df = stock.get_market_cap_by_date("20190101", "20190131", "005930")

