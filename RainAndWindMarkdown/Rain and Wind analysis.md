# Watertown, MA Rain and Wind analysis


```python
import requests
import os
import numpy as np
import pandas as pd
import getweatherdata
import matplotlib.pyplot as plt
from ipywidgets import interact
import ipywidgets as widgets
from matplotlib.widgets import Slider, RangeSlider, CheckButtons
#the next two are not needed in newer versions of Jupyter, Python
from IPython.display import display
%matplotlib inline
```


```python
#cannot use pd.read_csv because the file is not in the correct format
#use np.genfromtxt instead to read from fixed-width text file
#fields are unicode strings of prescribed length or double

stations = np.genfromtxt(os.getcwd()+'/stationdata.txt', delimiter=[11,9,10,7,3,31,4,4,6],
                                         names=['id','latitude','longitude','elevation','state','name',
                                                'gsn','hcn','wmo'],
                                         dtype=['U11','d','d','d','U3','U31','U4','U4','U6'],
                                         autostrip=True)
```


```python
#find stations beginning with "Watertown" in Massachusetts
stations[np.logical_and(np.char.find(stations['name'],'WATERTOWN')==0,stations['state']=='MA')]
```




    array([('US1MAMD0119', 42.3711, -71.1995, 16.5, 'MA', 'WATERTOWN 1.1 W', '', '', ''),
           ('US1MAMD0186', 42.3786, -71.1959, 36. , 'MA', 'WATERTOWN 1.1 NW', '', '', '')],
          dtype=[('id', '<U11'), ('latitude', '<f8'), ('longitude', '<f8'), ('elevation', '<f8'), ('state', '<U3'), ('name', '<U31'), ('gsn', '<U4'), ('hcn', '<U4'), ('wmo', '<U6')])



Both stations in Watertown, MA, are not in any of the quality-controlled large networks, so may only have limited data.


```python
response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/US1MAMD0119.dly')
with open('WatertownW.dly', 'w') as file:
    file.write(response.text)
```


```python
getweatherdata.dly_to_csv('WatertownW.dly','WATERTOWNW')
```


```python
response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/US1MAMD0186.dly')
with open('WatertownNW.dly', 'w') as file:
    file.write(response.text)
```


```python
getweatherdata.dly_to_csv('WatertownNW.dly','WATERTOWNNW')
```

The following are features of interest for WIND as per the [documentation](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt):
* AWDR = Average daily wind direction (degrees)
* AWND = Average daily wind speed (tenths of meters per second)
* WDF1 = Direction of fastest 1-minute wind (degrees)
* WDF2 = Direction of fastest 2-minute wind (degrees)
* WDF5 = Direction of fastest 5-second wind (degrees)
* WDFG = Direction of peak wind gust (degrees)
* WDFI = Direction of highest instantaneous wind (degrees)
* WDFM = Fastest mile wind direction (degrees)
* WDMV = 24-hour wind movement (km or miles as per user preference, miles on Daily Form pdf file)
* WSF1 = Fastest 1-minute wind speed (miles per hour or meters per second as per user preference)
* WSF2 = Fastest 2-minute wind speed (miles per hour or meters per second as per user preference)
* WSF5 = Fastest 5-second wind speed (miles per hour or meters per second as per user preference)
* WSFG = Peak guest wind speed (miles per hour or meters per second as per user preference)
* WSFI = Highest instantaneous wind speed (miles per hour or meters per second as per user preference)
* WSFM = Fastest mile wind speed (miles per hour or meters per second as per user preference)


```python
Watertown1=pd.read_csv('WATERTOWNW.csv')
Watertown1.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>STATION</th>
      <th>DATE</th>
      <th>PRCP</th>
      <th>PRCP_ATTRIBUTES</th>
      <th>SNOW</th>
      <th>SNOW_ATTRIBUTES</th>
      <th>SNWD</th>
      <th>SNWD_ATTRIBUTES</th>
      <th>WESD</th>
      <th>WESD_ATTRIBUTES</th>
      <th>WESF</th>
      <th>WESF_ATTRIBUTES</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>1</th>
      <td>US1MAMD0119</td>
      <td>2018-05-04</td>
      <td>13.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>2</th>
      <td>US1MAMD0119</td>
      <td>2018-05-05</td>
      <td>3.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>3</th>
      <td>US1MAMD0119</td>
      <td>2018-05-06</td>
      <td>0.0</td>
      <td>T,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>4</th>
      <td>US1MAMD0119</td>
      <td>2018-05-07</td>
      <td>71.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
    </tr>
  </tbody>
</table>
</div>




```python
Watertown2=pd.read_csv('WATERTOWNNW.csv')
Watertown2.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>STATION</th>
      <th>DATE</th>
      <th>DAPR</th>
      <th>DAPR_ATTRIBUTES</th>
      <th>MDPR</th>
      <th>MDPR_ATTRIBUTES</th>
      <th>PRCP</th>
      <th>PRCP_ATTRIBUTES</th>
      <th>SNOW</th>
      <th>SNOW_ATTRIBUTES</th>
      <th>WESF</th>
      <th>WESF_ATTRIBUTES</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>US1MAMD0186</td>
      <td>2021-03-07</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>US1MAMD0186</td>
      <td>2021-03-08</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>US1MAMD0186</td>
      <td>2021-03-09</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>US1MAMD0186</td>
      <td>2021-03-10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>US1MAMD0186</td>
      <td>2021-03-11</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>0.0</td>
      <td>,,N</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



For wind data, find a nearby station that has more data. We try one that is part of the WMO (world meteorological organization).


```python
#find stations beginning with 'BOSTON' in Massachusetts, one (Boston Logan) has a WMO ID
stations[np.logical_and(np.char.find(stations['name'],'BOSTON')==0,stations['state']=='MA')]
```




    array([('US1MASF0001', 42.357 , -71.0671, 13.1, 'MA', 'BOSTON 0.5 WSW', '', '', ''),
           ('US1MASF0031', 42.2927, -71.1456, 54.6, 'MA', 'BOSTON 6.5 SW', '', '', ''),
           ('USC00190768', 42.35  , -71.0667,  5.2, 'MA', 'BOSTON', '', '', ''),
           ('USW00014739', 42.3606, -71.0097,  3.4, 'MA', 'BOSTON', '', '', '72509'),
           ('USW00094701', 42.35  , -71.0667,  6.1, 'MA', 'BOSTON CITY WSO', '', '', '')],
          dtype=[('id', '<U11'), ('latitude', '<f8'), ('longitude', '<f8'), ('elevation', '<f8'), ('state', '<U3'), ('name', '<U31'), ('gsn', '<U4'), ('hcn', '<U4'), ('wmo', '<U6')])




```python
#find stations beginning with "CAMBRIDGE" in Massachusetts
stations[np.logical_and(np.char.find(stations['name'],'CAMBRIDGE')==0,stations['state']=='MA')]
```




    array([('US1MAMD0011', 42.3876, -71.1253, 14.6, 'MA', 'CAMBRIDGE 0.9 NNW', '', '', ''),
           ('US1MAMD0151', 42.3644, -71.1087,  5.2, 'MA', 'CAMBRIDGE 0.9 SSE', '', '', ''),
           ('USC00191097', 42.3833, -71.1167, 18. , 'MA', 'CAMBRIDGE', '', '', ''),
           ('USC00191099', 42.3833, -71.1   ,  2.4, 'MA', 'CAMBRIDGE "B"', '', '', ''),
           ('USC00191103', 42.375 , -71.1056,  4. , 'MA', 'CAMBRIDGE "C"', '', '', ''),
           ('USC00191110', 42.3667, -71.1   ,  5.8, 'MA', 'CAMBRIDGE MIT', '', '', '')],
          dtype=[('id', '<U11'), ('latitude', '<f8'), ('longitude', '<f8'), ('elevation', '<f8'), ('state', '<U3'), ('name', '<U31'), ('gsn', '<U4'), ('hcn', '<U4'), ('wmo', '<U6')])




```python
#the Cambridge stations do not have a WMO id, so we will stick with Boston Logan
response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00014739.dly')
with open('BostonLogan.dly', 'w') as file:
    file.write(response.text)
getweatherdata.dly_to_csv('BostonLogan.dly','BOSTONLOGAN')
```


```python
BostonLogan=pd.read_csv('BOSTONLOGAN.csv',low_memory=False) #low_memory=False suppresses a warning about mixed data types in columns 
BostonLogan.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>STATION</th>
      <th>DATE</th>
      <th>ACMH</th>
      <th>ACMH_ATTRIBUTES</th>
      <th>ACSH</th>
      <th>ACSH_ATTRIBUTES</th>
      <th>ADPT</th>
      <th>ADPT_ATTRIBUTES</th>
      <th>ASLP</th>
      <th>ASLP_ATTRIBUTES</th>
      <th>...</th>
      <th>WT17</th>
      <th>WT17_ATTRIBUTES</th>
      <th>WT18</th>
      <th>WT18_ATTRIBUTES</th>
      <th>WT19</th>
      <th>WT19_ATTRIBUTES</th>
      <th>WT21</th>
      <th>WT21_ATTRIBUTES</th>
      <th>WT22</th>
      <th>WT22_ATTRIBUTES</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USW00014739</td>
      <td>1936-01-01</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USW00014739</td>
      <td>1936-01-02</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>,,X</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USW00014739</td>
      <td>1936-01-03</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USW00014739</td>
      <td>1936-01-04</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USW00014739</td>
      <td>1936-01-05</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>,,X</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 108 columns</p>
</div>



## Filtering Data

Now, trim down the columns to include only precipitation, temperature, and wind data.


```python
#filter data for wind direction and speed, as well as temperature, from Boston Logan weather station
cols=list(BostonLogan.columns.values)
cols
```




    ['STATION',
     'DATE',
     'ACMH',
     'ACMH_ATTRIBUTES',
     'ACSH',
     'ACSH_ATTRIBUTES',
     'ADPT',
     'ADPT_ATTRIBUTES',
     'ASLP',
     'ASLP_ATTRIBUTES',
     'ASTP',
     'ASTP_ATTRIBUTES',
     'AWBT',
     'AWBT_ATTRIBUTES',
     'AWND',
     'AWND_ATTRIBUTES',
     'FMTM',
     'FMTM_ATTRIBUTES',
     'FRGT',
     'FRGT_ATTRIBUTES',
     'PGTM',
     'PGTM_ATTRIBUTES',
     'PRCP',
     'PRCP_ATTRIBUTES',
     'PSUN',
     'PSUN_ATTRIBUTES',
     'RHAV',
     'RHAV_ATTRIBUTES',
     'RHMN',
     'RHMN_ATTRIBUTES',
     'RHMX',
     'RHMX_ATTRIBUTES',
     'SNOW',
     'SNOW_ATTRIBUTES',
     'SNWD',
     'SNWD_ATTRIBUTES',
     'TAVG',
     'TAVG_ATTRIBUTES',
     'THIC',
     'THIC_ATTRIBUTES',
     'TMAX',
     'TMAX_ATTRIBUTES',
     'TMIN',
     'TMIN_ATTRIBUTES',
     'TSUN',
     'TSUN_ATTRIBUTES',
     'WDF1',
     'WDF1_ATTRIBUTES',
     'WDF2',
     'WDF2_ATTRIBUTES',
     'WDF5',
     'WDF5_ATTRIBUTES',
     'WDFG',
     'WDFG_ATTRIBUTES',
     'WDFM',
     'WDFM_ATTRIBUTES',
     'WESD',
     'WESD_ATTRIBUTES',
     'WSF1',
     'WSF1_ATTRIBUTES',
     'WSF2',
     'WSF2_ATTRIBUTES',
     'WSF5',
     'WSF5_ATTRIBUTES',
     'WSFG',
     'WSFG_ATTRIBUTES',
     'WSFM',
     'WSFM_ATTRIBUTES',
     'WT01',
     'WT01_ATTRIBUTES',
     'WT02',
     'WT02_ATTRIBUTES',
     'WT03',
     'WT03_ATTRIBUTES',
     'WT04',
     'WT04_ATTRIBUTES',
     'WT05',
     'WT05_ATTRIBUTES',
     'WT06',
     'WT06_ATTRIBUTES',
     'WT07',
     'WT07_ATTRIBUTES',
     'WT08',
     'WT08_ATTRIBUTES',
     'WT09',
     'WT09_ATTRIBUTES',
     'WT10',
     'WT10_ATTRIBUTES',
     'WT11',
     'WT11_ATTRIBUTES',
     'WT13',
     'WT13_ATTRIBUTES',
     'WT14',
     'WT14_ATTRIBUTES',
     'WT15',
     'WT15_ATTRIBUTES',
     'WT16',
     'WT16_ATTRIBUTES',
     'WT17',
     'WT17_ATTRIBUTES',
     'WT18',
     'WT18_ATTRIBUTES',
     'WT19',
     'WT19_ATTRIBUTES',
     'WT21',
     'WT21_ATTRIBUTES',
     'WT22',
     'WT22_ATTRIBUTES']




```python
mask=list(pd.Series(cols).str.match('^(AW|WD|WS|TM)[^B]\w{1}$')) #columns starting AW, WD, WS, or TM, not followed by B,
#4 characters only (so no flag columns)
cols=[col for i,col in enumerate(cols) if mask[i]]
cols
```




    ['AWND',
     'TMAX',
     'TMIN',
     'WDF1',
     'WDF2',
     'WDF5',
     'WDFG',
     'WDFM',
     'WSF1',
     'WSF2',
     'WSF5',
     'WSFG',
     'WSFM']




```python
#now restrict the columns to cols+identifiers, and restrict the date range
BostonLogan=BostonLogan[['STATION','DATE']+cols]
BostonLogan=BostonLogan[BostonLogan['DATE']>='2022-01-01']
#keep only columns which have at least one non-null entry
BostonLogan=BostonLogan[BostonLogan.columns[BostonLogan.notnull().sum()>0]]
BostonLogan.head(20)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>STATION</th>
      <th>DATE</th>
      <th>AWND</th>
      <th>TMAX</th>
      <th>TMIN</th>
      <th>WDF2</th>
      <th>WDF5</th>
      <th>WSF2</th>
      <th>WSF5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>31412</th>
      <td>USW00014739</td>
      <td>2022-01-01</td>
      <td>15.0</td>
      <td>111.0</td>
      <td>67.0</td>
      <td>120.0</td>
      <td>120.0</td>
      <td>36.0</td>
      <td>49.0</td>
    </tr>
    <tr>
      <th>31413</th>
      <td>USW00014739</td>
      <td>2022-01-02</td>
      <td>40.0</td>
      <td>78.0</td>
      <td>6.0</td>
      <td>310.0</td>
      <td>320.0</td>
      <td>103.0</td>
      <td>130.0</td>
    </tr>
    <tr>
      <th>31414</th>
      <td>USW00014739</td>
      <td>2022-01-03</td>
      <td>63.0</td>
      <td>6.0</td>
      <td>-60.0</td>
      <td>20.0</td>
      <td>330.0</td>
      <td>89.0</td>
      <td>121.0</td>
    </tr>
    <tr>
      <th>31415</th>
      <td>USW00014739</td>
      <td>2022-01-04</td>
      <td>44.0</td>
      <td>-5.0</td>
      <td>-82.0</td>
      <td>310.0</td>
      <td>330.0</td>
      <td>76.0</td>
      <td>98.0</td>
    </tr>
    <tr>
      <th>31416</th>
      <td>USW00014739</td>
      <td>2022-01-05</td>
      <td>50.0</td>
      <td>106.0</td>
      <td>-27.0</td>
      <td>180.0</td>
      <td>180.0</td>
      <td>107.0</td>
      <td>161.0</td>
    </tr>
    <tr>
      <th>31417</th>
      <td>USW00014739</td>
      <td>2022-01-06</td>
      <td>48.0</td>
      <td>61.0</td>
      <td>0.0</td>
      <td>290.0</td>
      <td>300.0</td>
      <td>98.0</td>
      <td>125.0</td>
    </tr>
    <tr>
      <th>31418</th>
      <td>USW00014739</td>
      <td>2022-01-07</td>
      <td>60.0</td>
      <td>6.0</td>
      <td>-49.0</td>
      <td>280.0</td>
      <td>270.0</td>
      <td>103.0</td>
      <td>130.0</td>
    </tr>
    <tr>
      <th>31419</th>
      <td>USW00014739</td>
      <td>2022-01-08</td>
      <td>48.0</td>
      <td>-21.0</td>
      <td>-82.0</td>
      <td>310.0</td>
      <td>330.0</td>
      <td>103.0</td>
      <td>134.0</td>
    </tr>
    <tr>
      <th>31420</th>
      <td>USW00014739</td>
      <td>2022-01-09</td>
      <td>72.0</td>
      <td>61.0</td>
      <td>-60.0</td>
      <td>230.0</td>
      <td>230.0</td>
      <td>143.0</td>
      <td>197.0</td>
    </tr>
    <tr>
      <th>31421</th>
      <td>USW00014739</td>
      <td>2022-01-10</td>
      <td>75.0</td>
      <td>44.0</td>
      <td>-55.0</td>
      <td>280.0</td>
      <td>280.0</td>
      <td>112.0</td>
      <td>161.0</td>
    </tr>
    <tr>
      <th>31422</th>
      <td>USW00014739</td>
      <td>2022-01-11</td>
      <td>59.0</td>
      <td>-55.0</td>
      <td>-132.0</td>
      <td>310.0</td>
      <td>330.0</td>
      <td>107.0</td>
      <td>143.0</td>
    </tr>
    <tr>
      <th>31423</th>
      <td>USW00014739</td>
      <td>2022-01-12</td>
      <td>58.0</td>
      <td>56.0</td>
      <td>-121.0</td>
      <td>220.0</td>
      <td>220.0</td>
      <td>134.0</td>
      <td>165.0</td>
    </tr>
    <tr>
      <th>31424</th>
      <td>USW00014739</td>
      <td>2022-01-13</td>
      <td>19.0</td>
      <td>78.0</td>
      <td>-16.0</td>
      <td>120.0</td>
      <td>180.0</td>
      <td>54.0</td>
      <td>63.0</td>
    </tr>
    <tr>
      <th>31425</th>
      <td>USW00014739</td>
      <td>2022-01-14</td>
      <td>73.0</td>
      <td>50.0</td>
      <td>-93.0</td>
      <td>310.0</td>
      <td>330.0</td>
      <td>116.0</td>
      <td>165.0</td>
    </tr>
    <tr>
      <th>31426</th>
      <td>USW00014739</td>
      <td>2022-01-15</td>
      <td>77.0</td>
      <td>-93.0</td>
      <td>-155.0</td>
      <td>320.0</td>
      <td>330.0</td>
      <td>125.0</td>
      <td>152.0</td>
    </tr>
    <tr>
      <th>31427</th>
      <td>USW00014739</td>
      <td>2022-01-16</td>
      <td>37.0</td>
      <td>17.0</td>
      <td>-149.0</td>
      <td>120.0</td>
      <td>110.0</td>
      <td>103.0</td>
      <td>125.0</td>
    </tr>
    <tr>
      <th>31428</th>
      <td>USW00014739</td>
      <td>2022-01-17</td>
      <td>107.0</td>
      <td>94.0</td>
      <td>17.0</td>
      <td>100.0</td>
      <td>120.0</td>
      <td>197.0</td>
      <td>250.0</td>
    </tr>
    <tr>
      <th>31429</th>
      <td>USW00014739</td>
      <td>2022-01-18</td>
      <td>81.0</td>
      <td>22.0</td>
      <td>-60.0</td>
      <td>280.0</td>
      <td>270.0</td>
      <td>134.0</td>
      <td>179.0</td>
    </tr>
    <tr>
      <th>31430</th>
      <td>USW00014739</td>
      <td>2022-01-19</td>
      <td>62.0</td>
      <td>78.0</td>
      <td>-66.0</td>
      <td>210.0</td>
      <td>230.0</td>
      <td>139.0</td>
      <td>192.0</td>
    </tr>
    <tr>
      <th>31431</th>
      <td>USW00014739</td>
      <td>2022-01-20</td>
      <td>49.0</td>
      <td>50.0</td>
      <td>-71.0</td>
      <td>330.0</td>
      <td>320.0</td>
      <td>98.0</td>
      <td>125.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#date restrict df1 and df2, and restrict the columns to station, date, precipitation, and snow
Watertown1=Watertown1[Watertown1['DATE']>='2022-01-01']
Watertown1=Watertown1[['STATION','DATE','PRCP','SNOW']]
Watertown2=Watertown2[Watertown2['DATE']>='2022-01-01']
Watertown2=Watertown2[['STATION','DATE','PRCP','SNOW']]
```


```python
Watertown1.head(20) #precipitation is given in tenths of mm
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>STATION</th>
      <th>DATE</th>
      <th>PRCP</th>
      <th>SNOW</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1328</th>
      <td>US1MAMD0119</td>
      <td>2022-01-01</td>
      <td>5.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1329</th>
      <td>US1MAMD0119</td>
      <td>2022-01-02</td>
      <td>76.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1330</th>
      <td>US1MAMD0119</td>
      <td>2022-01-03</td>
      <td>8.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1331</th>
      <td>US1MAMD0119</td>
      <td>2022-01-04</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1332</th>
      <td>US1MAMD0119</td>
      <td>2022-01-05</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1333</th>
      <td>US1MAMD0119</td>
      <td>2022-01-06</td>
      <td>76.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1334</th>
      <td>US1MAMD0119</td>
      <td>2022-01-07</td>
      <td>79.0</td>
      <td>170.0</td>
    </tr>
    <tr>
      <th>1335</th>
      <td>US1MAMD0119</td>
      <td>2022-01-08</td>
      <td>51.0</td>
      <td>43.0</td>
    </tr>
    <tr>
      <th>1336</th>
      <td>US1MAMD0119</td>
      <td>2022-01-09</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1337</th>
      <td>US1MAMD0119</td>
      <td>2022-01-10</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1338</th>
      <td>US1MAMD0119</td>
      <td>2022-01-11</td>
      <td>0.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1339</th>
      <td>US1MAMD0119</td>
      <td>2022-01-12</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1340</th>
      <td>US1MAMD0119</td>
      <td>2022-01-13</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1341</th>
      <td>US1MAMD0119</td>
      <td>2022-01-14</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1342</th>
      <td>US1MAMD0119</td>
      <td>2022-01-15</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1343</th>
      <td>US1MAMD0119</td>
      <td>2022-01-16</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1344</th>
      <td>US1MAMD0119</td>
      <td>2022-01-17</td>
      <td>203.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1345</th>
      <td>US1MAMD0119</td>
      <td>2022-01-18</td>
      <td>127.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1346</th>
      <td>US1MAMD0119</td>
      <td>2022-01-19</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1347</th>
      <td>US1MAMD0119</td>
      <td>2022-01-20</td>
      <td>15.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
Watertown2.head() #we see here that missing dates can occur (Jan 5, 2022 is missing), so need to take care of mapping dates correctly
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>STATION</th>
      <th>DATE</th>
      <th>PRCP</th>
      <th>SNOW</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>270</th>
      <td>US1MAMD0186</td>
      <td>2022-01-01</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>271</th>
      <td>US1MAMD0186</td>
      <td>2022-01-02</td>
      <td>81.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>272</th>
      <td>US1MAMD0186</td>
      <td>2022-01-03</td>
      <td>5.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>273</th>
      <td>US1MAMD0186</td>
      <td>2022-01-04</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>274</th>
      <td>US1MAMD0186</td>
      <td>2022-01-06</td>
      <td>71.0</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



## Plotting Data

### Quick plots

Plot temperature, precipitation, highlight special wind events (wind coming from ENE to ESE).


```python
#first quick plot of the temperature ... only important to gauge snowfall vs rain
plt.plot(BostonLogan['TMIN']/10)
plt.plot(BostonLogan['TMAX']/10)
```




    [<matplotlib.lines.Line2D at 0x143ebf70>]




    
![png](output_28_1.png)
    



```python
#first quick plot of precipitation/rain and snow in cm
days=np.arange(1,len(Watertown1)+1)
plt.bar(days,Watertown1['PRCP']/100)
plt.bar(days,Watertown1['SNOW']/100)
```




    <BarContainer object of 442 artists>




    
![png](output_29_1.png)
    



```python
#first quick plot of wind speed, highlighting wind coming from ENE to ESE directions (60 to 120 degrees from true North)
days=np.arange(1,len(BostonLogan)+1)
col=np.where((BostonLogan['WDF2']>=60) & (BostonLogan['WDF2']<=120),'c','k')
plt.scatter(days,BostonLogan['WSF2'],c=col,s=1)
```




    <matplotlib.collections.PathCollection at 0x13cb4bb0>




    
![png](output_30_1.png)
    


### Detailed plots


```python
#indexing by date
Watertown1.index=pd.DatetimeIndex(Watertown1.DATE)
Watertown2.index=pd.DatetimeIndex(Watertown2.DATE)
BostonLogan.index=pd.DatetimeIndex(BostonLogan.DATE)
```


```python
#reindex, filling in missing dates, so that all dataframes have the same index (NOW we have new objects with np.NaN filled)
today=pd.to_datetime('today').date()
Watertown1=Watertown1.reindex(pd.date_range("2022-01-01", today))
Watertown2=Watertown2.reindex(pd.date_range("2022-01-01", today))
BostonLogan=BostonLogan.reindex(pd.date_range("2022-01-01", today))
```


```python
Watertown2.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>STATION</th>
      <th>DATE</th>
      <th>PRCP</th>
      <th>SNOW</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2022-01-01</th>
      <td>US1MAMD0186</td>
      <td>2022-01-01</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2022-01-02</th>
      <td>US1MAMD0186</td>
      <td>2022-01-02</td>
      <td>81.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2022-01-03</th>
      <td>US1MAMD0186</td>
      <td>2022-01-03</td>
      <td>5.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2022-01-04</th>
      <td>US1MAMD0186</td>
      <td>2022-01-04</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2022-01-05</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
BostonLogan.tail() #there appears to be a several day lag in publishing the latest data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>STATION</th>
      <th>DATE</th>
      <th>AWND</th>
      <th>TMAX</th>
      <th>TMIN</th>
      <th>WDF2</th>
      <th>WDF5</th>
      <th>WSF2</th>
      <th>WSF5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-03-20</th>
      <td>USW00014739</td>
      <td>2023-03-20</td>
      <td>58.0</td>
      <td>111.0</td>
      <td>-22.0</td>
      <td>230.0</td>
      <td>250.0</td>
      <td>107.0</td>
      <td>134.0</td>
    </tr>
    <tr>
      <th>2023-03-21</th>
      <td>USW00014739</td>
      <td>2023-03-21</td>
      <td>NaN</td>
      <td>144.0</td>
      <td>11.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2023-03-22</th>
      <td>USW00014739</td>
      <td>2023-03-22</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2023-03-23</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2023-03-24</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
plt.figure(figsize=(10,4.5))
threshw=100 #wind threshold
threshr=100 #rain threshold
dirmin=60
dirmax=140
mask=((BostonLogan['WDF2']>=dirmin) & (BostonLogan['WDF2']<=dirmax) & (BostonLogan['WSF2']>=threshw)
      & ((Watertown1['PRCP']>=threshr) | (Watertown2['PRCP']>=threshr)))
plt.bar(Watertown1.index, Watertown1['PRCP'])
plt.scatter(BostonLogan.loc[mask].index,Watertown1.loc[mask]['PRCP'],marker='o')
plt.axis(xmin=pd.to_datetime('2022-01-01').date(),xmax=pd.to_datetime('today').date())
plt.ylabel('Precipitation [1/10 mm]')
plt.xticks(BostonLogan.loc[mask].index,rotation=90)
plt.title('Precipitation in Combination with strong Eastern winds in Watertown, MA');
```


    
![png](output_36_0.png)
    



```python
BostonLogan.loc[mask], Watertown1.loc[mask], Watertown2.loc[mask]
#we see the rainfall amounts are generally similar between the two Watertown stations, 
#and the average wind speed vs fastest 2-min wind (WSF2) gives us an
#idea about which days have sustained strong winds
```




    (                STATION        DATE   AWND   TMAX   TMIN   WDF2   WDF5   WSF2  \
     2022-01-17  USW00014739  2022-01-17  107.0   94.0   17.0  100.0  120.0  197.0   
     2022-03-24  USW00014739  2022-03-24   75.0   61.0   39.0  110.0  110.0  107.0   
     2022-04-08  USW00014739  2022-04-08   55.0  172.0   67.0  130.0  120.0  134.0   
     2022-04-19  USW00014739  2022-04-19   97.0  150.0   61.0  130.0   80.0  165.0   
     2022-10-14  USW00014739  2022-10-14   44.0  206.0  139.0  130.0  130.0  125.0   
     2022-11-16  USW00014739  2022-11-16   67.0  139.0   28.0  100.0  280.0  116.0   
     2022-12-16  USW00014739  2022-12-16  110.0   72.0   56.0   70.0   60.0  143.0   
     2023-01-20  USW00014739  2023-01-20   45.0   33.0   -5.0   60.0   60.0  161.0   
     2023-03-04  USW00014739  2023-03-04   93.0   28.0   -6.0   80.0   90.0  165.0   
     
                  WSF5  
     2022-01-17  250.0  
     2022-03-24  130.0  
     2022-04-08  170.0  
     2022-04-19  206.0  
     2022-10-14  157.0  
     2022-11-16  152.0  
     2022-12-16  183.0  
     2023-01-20  192.0  
     2023-03-04  201.0  ,
                     STATION        DATE   PRCP  SNOW
     2022-01-17  US1MAMD0119  2022-01-17  203.0   0.0
     2022-03-24  US1MAMD0119  2022-03-24  102.0   0.0
     2022-04-08  US1MAMD0119  2022-04-08  117.0   0.0
     2022-04-19  US1MAMD0119  2022-04-19  300.0   0.0
     2022-10-14  US1MAMD0119  2022-10-14  330.0   0.0
     2022-11-16  US1MAMD0119  2022-11-16  175.0   0.0
     2022-12-16  US1MAMD0119  2022-12-16  170.0   0.0
     2023-01-20  US1MAMD0119  2023-01-20  269.0   5.0
     2023-03-04  US1MAMD0119  2023-03-04  130.0   NaN,
                     STATION        DATE   PRCP  SNOW
     2022-01-17  US1MAMD0186  2022-01-17  198.0   NaN
     2022-03-24  US1MAMD0186  2022-03-24   89.0   NaN
     2022-04-08  US1MAMD0186  2022-04-08  117.0   NaN
     2022-04-19  US1MAMD0186  2022-04-19  295.0   NaN
     2022-10-14  US1MAMD0186  2022-10-14  287.0   NaN
     2022-11-16  US1MAMD0186  2022-11-16  145.0   NaN
     2022-12-16  US1MAMD0186  2022-12-16  137.0   NaN
     2023-01-20  US1MAMD0186  2023-01-20  267.0   NaN
     2023-03-04  US1MAMD0186  2023-03-04  124.0   NaN)




```python
#%matplotlib notebook
#uncomment the above to have interactive output (functional sliders, etc.) for this cell, or simply run the next cell

#initialize plot
fig,ax=plt.subplots(figsize=(20,4.5))

ax.set_ylabel('Precipitation [1/10 mm]')
ax.set_title('Precipitation in combination with strong Eastern winds in Watertown, MA')
ax.set_xlim(xmin=pd.to_datetime('2022-01-01').date(),xmax=pd.to_datetime('today').date())
plt.setp(ax.get_xticklabels(),rotation=90)

dirmin_init=60
dirmax_init=140
threshr_init=100
threshw_init=100
mask=((BostonLogan['WDF2']>=dirmin_init) & (BostonLogan['WDF2']<=dirmax_init) & (BostonLogan['AWND']>=threshw_init) & (Watertown1['PRCP']>=threshr_init))
col=np.where(mask,'r','k')
bars=ax.bar(Watertown1.index,Watertown1['PRCP'],color=col)#initialize bar plot with colored bars
for i in range(len(bars)): #also adjust opacity
    if mask[i]:
        bars[i].set(alpha=1)
    else:
        bars[i].set(alpha=0.3)
ticks=ax.set_xticks(BostonLogan.loc[mask].index)#point out colored bars with tick labels
#plt.show()

#plot update function
def weatherplot(threshr,threshw,direction,complement):
    #use AWND to gauge sustained strong wind
    mask= (BostonLogan['AWND']>=threshw) & (Watertown1['PRCP']>=threshr)
    if complement:
        mask=mask&((BostonLogan['WDF2']<=direction[0]) | (BostonLogan['WDF2']>=direction[1]))
    else:
        mask=mask&(BostonLogan['WDF2']>=direction[0]) & (BostonLogan['WDF2']<=direction[1])
    for i in range(len(bars)):
        if mask[i]:
            bars[i].set(color='r',alpha=1)
        else:
            bars[i].set(color='k',alpha=0.3)
    ticks=ax.set_xticks(BostonLogan.loc[mask].index)
    fig.canvas.draw_idle()

#make room for the sliders
fig.subplots_adjust(left=0.1, bottom=0.5)

#create new axes, sliders, and checkbox
axr=fig.add_axes([0.03, 0.5, 0.01, 0.38])
r_slider=Slider(ax=axr,valinit=threshr_init,valmin=0,valmax=400,label='rain threshold',orientation='vertical')
axw=fig.add_axes([0.1, 0.2, 0.2, 0.04])
w_slider=Slider(ax=axw,valinit=threshw_init,valmin=0,valmax=400,label='wind threshold')
axd=fig.add_axes([0.1, 0.1, 0.2, 0.04])
d_slider=RangeSlider(ax=axd,valinit=[dirmin_init,dirmax_init],valmin=0,valmax=360,label='wind direction')
axc=fig.add_axes([0.35, 0.1, 0.2, 0.04])
c_box=CheckButtons(ax=axc,labels=['use complement of direction interval'])

#update function accepts exactly one (dummy) argument
def update(arg):
    weatherplot(r_slider.val,w_slider.val,d_slider.val,c_box.get_status()[0]) 
    #vals of sliders and the status of the first (and only) checkbutton passed to the actual update function weatherplot()

#register sliders and checkbox with the update function
r_slider.on_changed(update)
w_slider.on_changed(update)
d_slider.on_changed(update)
c_box.on_clicked(update);
```


    
![png](output_38_0.png)
    



```python
#%matplotlib inline
#run the notebook in order to use the widgets and see the output
fig,ax=plt.subplots(figsize=(20,4.5))

ax.set_ylabel('Precipitation [1/10 mm]')
ax.set_title('Precipitation in combination with strong Eastern winds in Watertown, MA')
ax.set_xlim(xmin=pd.to_datetime('2022-01-01').date(),xmax=pd.to_datetime('today').date())
plt.setp(ax.get_xticklabels(),rotation=90)
#plt.setp(ax,visible=False) #this only makes the first plot "blank", but doesn't stop it from appearing

bars=ax.bar(Watertown1.index,Watertown1['PRCP'])#initialize bar plot
plt.close(fig)#don't show figure (yet), stops first plot from appearing

#plot update function
def weatherplot(threshr,threshw,direction,complement):
    #plt.clf() #does not remove the plot drawn outside of this function
    #use AWND to gauge sustained strong wind
    mask= (BostonLogan['AWND']>=threshw) & (Watertown1['PRCP']>=threshr)
    if complement:
        mask&=((BostonLogan['WDF2']<=direction[0]) | (BostonLogan['WDF2']>=direction[1]))
    else:
        mask&=(BostonLogan['WDF2']>=direction[0]) & (BostonLogan['WDF2']<=direction[1])
    for i in range(len(bars)):
        if mask[i]:
            bars[i].set(color='r',alpha=1)
        else:
            bars[i].set(color='k',alpha=0.3)
    ticks=ax.set_xticks(BostonLogan.loc[mask].index)
    #plt.show() ... does not seem to do the trick
    #fig.canvas.draw_idle() ... does not seem to do the trick
    display(fig)
    #return fig#same effect as display(), this redraws the figure below, but it doesn't close/update the figure if drawn outside this function

r_slider=widgets.IntSlider(value=100,min=0,max=400,step=1, description='rain threshold', continuous_update=False)
w_slider=widgets.IntSlider(value=100,min=0,max=400,step=1,description='wind threshold', continuous_update=False)
d_slider=widgets.IntRangeSlider(value=[60,140],min=0,max=360,step=1,description='wind direction', continuous_update=False)
c_box=widgets.Checkbox(value=False,description='use complement of direction interval',disabled=False,indent=False)


interact(weatherplot,threshr=r_slider,threshw=w_slider,direction=d_slider,complement=c_box);

```


    interactive(children=(IntSlider(value=100, continuous_update=False, description='rain threshold', max=400), In…



```python

```
