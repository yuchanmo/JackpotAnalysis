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

df = pd.DataFrame(parsed_res,columns=['분류','종목','추천일','목표일','매수저점','매수고점','목표가','손절가'])