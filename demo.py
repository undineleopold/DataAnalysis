import requests
import os
import numpy as np
import pandas as pd
import weatherdata as w
import matplotlib.pyplot as plt


stations = np.genfromtxt(os.getcwd()+'/stationdata.txt', delimiter=[11,9,10,7,3,31,4,4,6],
                                         names=['id','latitude','longitude','elevation','state','name',
                                                'gsn','hcn','wmo'],
                                         dtype=['U11','d','d','d','U3','U31','U4','U4','U6'],
                                         autostrip=True)

reload=input('reload? y/n: ')
if reload=='y':
    response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00014739.dly')
    with open('BostonLogan.dly', 'w') as file:
        file.write(response.text)
    BostonLogan=w.dly_to_csv('BostonLogan.dly','BOSTONLOGAN')
else:
    BostonLogan=pd.read_csv('BOSTONLOGAN.csv', low_memory=False)

print('Retrieved data')

#keep only columns which have at least one non-null entry
BostonLogan=BostonLogan[BostonLogan.columns[BostonLogan.notnull().sum()>0]]

cols=list(BostonLogan.columns.values)
mask=list(pd.Series(cols).str.match('^(AW|WD|WS|TM|PR)[^B]\w{1}$')) #columns starting AW, WD, WS, or TM, not followed by B,
#4 characters only (so no flag columns)
cols=[col for i,col in enumerate(cols) if mask[i]]

print('Fields available for analysis: ', cols)

#now restrict the columns to cols+identifying columns, and restrict the date range to the last couple years
BostonLogan=BostonLogan[['STATION','DATE']+cols]
BostonLogan=BostonLogan[BostonLogan['DATE']>='2020-01-01']

BostonLogan.index=pd.DatetimeIndex(BostonLogan.DATE)
today=pd.to_datetime('today').date()
BostonLogan=BostonLogan.reindex(pd.date_range("2020-01-01", today))

w.make_prcp20_plot(BostonLogan,'Rain and Wind in Boston, MA')
