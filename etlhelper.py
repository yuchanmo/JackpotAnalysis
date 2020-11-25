import pandas as pd 


def filterNewExistTable(left:pd.DataFrame,right:pd.DataFrame,leftkeys:list,rightkeys:list,colforexist:str,containsright:bool=False):
    try:
        merged = pd.merge(left,right,left_on=leftkeys,right_on=rightkeys,how='left',suffixes=['','_y'])
        colkey = colforexist+'_y' if colforexist + '_y' in list(merged) else colforexist
        new,exist = merged[merged[colkey].isnull()],merged[merged[colkey].notnull()]  
        leftcols = list(left)
        if containsright:
            return new,exist  
        else:
            return new[leftcols],exist[leftcols]
    except Exception as e:
        raise e
    
    

    