
import pandas as pd
from dbconnector import sqlserver
import matplotlib.pyplot as plt
import os

import matplotlib

matplotlib.rcParams['font.family'] ='Malgun Gothic'

matplotlib.rcParams['axes.unicode_minus'] =False

sql = '''
select  c.category
		,c.categoryname
		,cd.name
		,code.code
		,code.category as codecategory
		,d.date
		,case when (d.closeprice - d.pricediff) <> 0 then pricediff / cast(d.closeprice - d.pricediff as real) else 0 end as diffratio
from Category c
join CategoryDetail cd
	on c.CategoryId = cd.CategoryId
join Code code
	on cd.name = code.name
join DailyPrice d
	on d.code = code.code
where d.date between dateadd(d,-60,getdate()) and getdate()
'''
df = pd.read_sql(sql,sqlserver)
grouped_df = df.groupby(['category','categoryname','date'])[['diffratio']].agg('mean').reset_index()
grouped_df = grouped_df.set_index('date')
grouped_df['diffratio'] = grouped_df['diffratio']*100
gr = grouped_df.groupby(['category','categoryname'])


for gn,g in gr:
    print(gn)
    basepath = r'D:\Programming\stocktrading\trendanalyzer\result\20210406'    
    filename = str(gn).replace('(','').replace(')','').replace('/','_').replace(',','_')
    g['diffratio'].plot(title=str(gn),rot=90,figsize=(10,6),ylim=(-10,10))    
    plt.grid(True)        
    filefullpath = os.path.join(basepath,filename+'.png')
    plt.savefig(filefullpath)
    plt.clf()
    
    