
import pandas as pd
import pymysql
from dbconnector import *

con = pymysql.connect(host='dwemaria.westus.cloudapp.azure.com',port=3306,user='sa',passwd='1q2w3e4r5t6y',db='jackpotman')
d = pd.read_sql('select * from AriseCodeList',engine)
