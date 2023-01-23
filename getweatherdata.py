import numpy as np
import pandas as pd

def dly_to_df(filename):
    # load the fixed-width file following the format in readme.txt
    # and label the columns
    # note that each row contains an entire month (31 days, some data will be missing)
    colnames=['STATION','YEAR','MONTH','ELEMENT']
    for i in range(1,32): #how to do this in a single list comprehension?
        colnames.extend([f'day{i}', f'm{i}', f'q{i}', f's{i}'])
    data = np.genfromtxt(filename,
                      delimiter=[11,4,2,4] + [5,1,1,1]*31,
                      names=colnames,
                      dtype=['U11','i','i','U4'] + ['d','U1','U1','U1']*31,
                      autostrip=True)
    pdata=pd.DataFrame(data) #convert to pandas DataFrame
    return pdata


def dly_to_csv(filename, target=None):
    # load the fixed-width file following the format in readme.txt
    # and label the columns
    # note that each row contains an entire month (31 days, some data will be missing)
    colnames=['STATION','YEAR','MONTH','ELEMENT']
    for i in range(1,32): 
        colnames.extend([f'day{i}', f'm{i}', f'q{i}', f's{i}'])
    data = np.genfromtxt(filename,
                      delimiter=[11,4,2,4] + [5,1,1,1]*31,
                      names=colnames,
                      dtype=['U11','i','i','U4'] + ['d','U1','U1','U1']*31,
                      autostrip=True)
    pdata=pd.DataFrame(data) #convert to pandas DataFrame
    
    pdata = pd.melt(pdata, id_vars=['STATION','YEAR','MONTH','ELEMENT'])
    pdata['DAY']=pdata['variable'].apply(lambda x: int(x[3:]) if len(x)>3 else int(x[1:]))
    pdata['variable']=pdata['variable'].apply(lambda x: x[:3] if len(x)>3 else x[0])
    pdata=pd.pivot(pdata,index=['STATION','YEAR','MONTH','DAY','ELEMENT'],columns=['variable'], values='value')
    pdata.rename(columns={'day':'value'}, inplace=True)
    #throw out data for all days with 'invalid' measurements
    pdata = pdata[pdata.value != -9999]
    #such days are, e.g., Feb 30
    pdata.reset_index(inplace=True)
    # make a column 'date' out of year, month, day
    pdata['DATE'] = pd.to_datetime(pdata[['YEAR','MONTH','DAY']])
    pdata.columns.name=None
    #forget separate YEAR,MONTH,DAY columns
    pdata=pdata[['STATION','DATE','ELEMENT','value','m','q','s']]
    pdata['ATTRIBUTES']=pdata['m']+','+pdata['q']+','+pdata['s']
    #forget separate m, q, s columns
    pdata=pdata[['STATION','DATE','ELEMENT','value','ATTRIBUTES']]
    pdata = pdata.pivot(index=['STATION','DATE'], columns='ELEMENT')
    pdata.rename(columns={'value':''}, inplace=True)
    pdata.columns = ['_'.join(col).rstrip('_') for col in [c[::-1] for c in pdata.columns.values]]
    pdata=pdata[list(pdata.columns.sort_values())] #sort column names (elements, attributes) alphabetically
    pdata.reset_index(inplace=True)
    if not target:
        target=filename
    pdata.to_csv(target+'.csv', index=False)

