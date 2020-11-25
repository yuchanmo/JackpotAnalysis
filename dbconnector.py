from sqlalchemy import create_engine 
coninfo = {
    'user':'sa',
    'pwd':'1',
    'host':'DESKTOP-OM7PTBL',
    'database':'Stock'
}
sqlserver = create_engine(f"mssql+pymssql://{coninfo['user']}:{coninfo['pwd']}@{coninfo['host']}/{coninfo['database']}", echo=True)

#maria_engine = create_engine('mysql+pymysql://sa:1q2w3e4r5t6y@dwemaria.westus.cloudapp.azure.com/jackpotman')

