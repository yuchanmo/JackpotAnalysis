from dbconnector import sqlserver
from datetime import datetime,timedelta

def removeOldData(d:int = 2):
    old_days = timedelta(days=d)
    old_refs = datetime.today()-old_days
    old_date = old_refs.strftime('%Y-%m-%d')
    print(old_date)
    with sqlserver.connect() as con:
        con.execute(f"delete from Jackpot where Regdate < '{old_date}'")

    print(f"delete from Jackpot where Regdate < '{old_date}'")