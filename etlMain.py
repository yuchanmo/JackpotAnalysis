from etlCode import loadCode 
from etldailyprice import loadData
from etlKeyItem import loadKeyItem
from etlPriceAfterWorkinghour import loadPriceAfterWokringHour

if __name__ =='__main__':
    print('==========================================load code==========================================')
    loadCode()
    print('==========================================load daily price==========================================')
    loadData(2)
    print('==========================================load key item==========================================')
    loadKeyItem(None)
    print('==========================================load price after workinghours==========================================')
    loadPriceAfterWokringHour()
