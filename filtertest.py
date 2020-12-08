#%%
import pandas as pd
from dbconnector import sqlserver
sql = '''
select * 
from AllTimePriceFromNaver
where code in ('241840','001810','042000') and Regdate >='2020-12-08'

'''
#%%
df = pd.read_sql(sql,sqlserver)
df['Regdate'] = pd.to_datetime(df['Regdate'])
df = df.set_index(['Regdate'])
df.resample('3min')['curvol'].mean().plot()

# %%
vol3min = df.resample('3min')['curvol'].mean()
vol3min = pd.DataFrame(vol3min)

#%%
vol3min.shift(-1).head()
#%%
((vol3min - vol3min.shift(1))/vol3min.shift(1)).plot()
# %%
vol3min.plot()
# %%
cv = df[['curvol']]
cv['diff'] = (cv/cv.shift(1)-1)*100

# %%
np.diff(np.sign([1,2,3,-1]))
np.gradient([1,5,3,4,2,2,3,4])
import numpy as np
f_prime = np.gradient(cv['curvol']) # differential approximation
indices = np.where (np.diff (np.sign (f_prime))) [0] # Find the inflection point.
infections = cv.iloc[indices]
# %%

def findInflectionPoint(valarr):
    f_prime = np.gradient(valarr) # differential approximation
    indices = np.where (np.diff (np.sign (f_prime))) [0] # Find the inflection point.
    return indices


for gn,s in df.groupby('code'):
    print(gn)
    i = findInflectionPoint(s['curvol'])
    ife = s.iloc[i]

    plt.plot(s.index,s['curvol'])
    plt.plot(ife.index,ife['curvol'],'x')
    plt.show()


ss = df[df['code'] == '241840']
((ss['curvol']/ss['curvol'].shift(1)-1)*100).plot()
plt.show()
ss['curvol'].plot()
m = ss[ss['curvol']>0]['curvol'].min()

((ss['curvol']/m)*100).plot()
plt.show()
ss['curvol'].plot().show()
s = cv[:'2020-12-08 11:30']
i = findInflectionPoint(s['curvol'])
ife = s.iloc[i]

plt.plot(s.index,s['curvol'])
plt.plot(ife.index,ife['curvol'],'x')
plt.show()


import matplotlib.pyplot as plt
plt.plot(cv.index,cv['curvol'])
plt.plot(infections.index,infections['curvol'],'x')
plt.show()

y = np.arange(0,100)
y[10:] = y[10:]**y[10:]
x = np.arange(0,100)
i = findInflectionPoint(y)


plt.plot(x,y)
plt.plot(x[i],y[i],'x')
plt.show()