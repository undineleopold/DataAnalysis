# Watertown, MA Rain and Wind analysis


```python
import requests
import os
import numpy as np
import pandas as pd
from weatherdata import get_stations, dly_to_csv
import matplotlib.pyplot as plt
from matplotlib.dates import num2date
from ipywidgets import interact
import ipywidgets as widgets
from matplotlib.widgets import RadioButtons, Slider, RangeSlider, CheckButtons
#the next two are not needed in newer versions of Jupyter, Python
from IPython.display import display
%matplotlib inline
```


```python
stations = get_stations('stationdata.txt')
```


```python
#find stations beginning with "Watertown" in Massachusetts
stations[np.logical_and(np.char.find(stations['name'],'WATERTOWN')==0,stations['state']=='MA')]
```




    array([('US1MAMD0119', 42.3711, -71.1995, 16.5, 'MA', 'WATERTOWN 1.1 W', '', '', ''),
           ('US1MAMD0186', 42.3786, -71.1959, 36. , 'MA', 'WATERTOWN 1.1 NW', '', '', '')],
          dtype=[('id', '<U11'), ('latitude', '<f8'), ('longitude', '<f8'), ('elevation', '<f8'), ('state', '<U3'), ('name', '<U31'), ('gsn', '<U4'), ('hcn', '<U4'), ('wmo', '<U6')])



Neither station in Watertown, MA, has a GSN, HCN, or WMO network ID, so data may be limited. Let's download and reformat the data from both stations.


```python
response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/US1MAMD0119.dly')
with open('WatertownW.dly', 'w') as file:
    file.write(response.text)
```


```python
Watertown1=dly_to_csv('WatertownW.dly','WATERTOWNW')
Watertown1.head()
```




<div>

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
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>1</th>
      <td>US1MAMD0119</td>
      <td>2018-05-04</td>
      <td>13</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>2</th>
      <td>US1MAMD0119</td>
      <td>2018-05-05</td>
      <td>3</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>3</th>
      <td>US1MAMD0119</td>
      <td>2018-05-06</td>
      <td>0</td>
      <td>T,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>4</th>
      <td>US1MAMD0119</td>
      <td>2018-05-07</td>
      <td>71</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
  </tbody>
</table>
</div>




```python
response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/US1MAMD0186.dly')
with open('WatertownNW.dly', 'w') as file:
    file.write(response.text)
```


```python
Watertown2=dly_to_csv('WatertownNW.dly','WATERTOWNNW')
Watertown2.head()
```




<div>

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
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
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
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
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
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
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
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
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
      <td>0</td>
      <td>,,N</td>
      <td>0</td>
      <td>,,N</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



Both stations are fairly close together, and the second station has data going further back, so we continue using that one (WATERTOWNW, dataframe Watertown1) exclusively. However, we see no wind data is recorded.

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
BostonLogan=dly_to_csv('BostonLogan.dly','BOSTONLOGAN')
BostonLogan.head()
```




<div>

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
      <td>1</td>
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
      <td>1</td>
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

For this analysis, we mainly focus on precipitation and wind. Trim down the columns a bit.


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
#now restrict the columns to cols+identifying columns, and restrict the date range to the last couple years
BostonLogan=BostonLogan[['STATION','DATE']+cols]
BostonLogan=BostonLogan[BostonLogan['DATE']>='2020-01-01']
#keep only columns which have at least one non-null entry
BostonLogan=BostonLogan[BostonLogan.columns[BostonLogan.notnull().sum()>0]]
BostonLogan.head(20)
```




<div>

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
      <th>30681</th>
      <td>USW00014739</td>
      <td>2020-01-01</td>
      <td>69</td>
      <td>61</td>
      <td>22</td>
      <td>260</td>
      <td>250</td>
      <td>130</td>
      <td>188</td>
    </tr>
    <tr>
      <th>30682</th>
      <td>USW00014739</td>
      <td>2020-01-02</td>
      <td>56</td>
      <td>94</td>
      <td>11</td>
      <td>280</td>
      <td>250</td>
      <td>94</td>
      <td>125</td>
    </tr>
    <tr>
      <th>30683</th>
      <td>USW00014739</td>
      <td>2020-01-03</td>
      <td>32</td>
      <td>111</td>
      <td>67</td>
      <td>230</td>
      <td>230</td>
      <td>76</td>
      <td>94</td>
    </tr>
    <tr>
      <th>30684</th>
      <td>USW00014739</td>
      <td>2020-01-04</td>
      <td>24</td>
      <td>89</td>
      <td>44</td>
      <td>350</td>
      <td>360</td>
      <td>63</td>
      <td>81</td>
    </tr>
    <tr>
      <th>30685</th>
      <td>USW00014739</td>
      <td>2020-01-05</td>
      <td>74</td>
      <td>50</td>
      <td>0</td>
      <td>310</td>
      <td>320</td>
      <td>139</td>
      <td>183</td>
    </tr>
    <tr>
      <th>30686</th>
      <td>USW00014739</td>
      <td>2020-01-06</td>
      <td>30</td>
      <td>50</td>
      <td>-27</td>
      <td>250</td>
      <td>240</td>
      <td>94</td>
      <td>134</td>
    </tr>
    <tr>
      <th>30687</th>
      <td>USW00014739</td>
      <td>2020-01-07</td>
      <td>41</td>
      <td>56</td>
      <td>6</td>
      <td>270</td>
      <td>260</td>
      <td>98</td>
      <td>116</td>
    </tr>
    <tr>
      <th>30688</th>
      <td>USW00014739</td>
      <td>2020-01-08</td>
      <td>63</td>
      <td>72</td>
      <td>-16</td>
      <td>280</td>
      <td>280</td>
      <td>134</td>
      <td>179</td>
    </tr>
    <tr>
      <th>30689</th>
      <td>USW00014739</td>
      <td>2020-01-09</td>
      <td>59</td>
      <td>6</td>
      <td>-55</td>
      <td>300</td>
      <td>300</td>
      <td>116</td>
      <td>161</td>
    </tr>
    <tr>
      <th>30690</th>
      <td>USW00014739</td>
      <td>2020-01-10</td>
      <td>62</td>
      <td>117</td>
      <td>-16</td>
      <td>230</td>
      <td>240</td>
      <td>130</td>
      <td>161</td>
    </tr>
    <tr>
      <th>30691</th>
      <td>USW00014739</td>
      <td>2020-01-11</td>
      <td>81</td>
      <td>211</td>
      <td>94</td>
      <td>230</td>
      <td>200</td>
      <td>174</td>
      <td>215</td>
    </tr>
    <tr>
      <th>30692</th>
      <td>USW00014739</td>
      <td>2020-01-12</td>
      <td>93</td>
      <td>233</td>
      <td>44</td>
      <td>210</td>
      <td>220</td>
      <td>161</td>
      <td>197</td>
    </tr>
    <tr>
      <th>30693</th>
      <td>USW00014739</td>
      <td>2020-01-13</td>
      <td>41</td>
      <td>61</td>
      <td>22</td>
      <td>20</td>
      <td>20</td>
      <td>76</td>
      <td>94</td>
    </tr>
    <tr>
      <th>30694</th>
      <td>USW00014739</td>
      <td>2020-01-14</td>
      <td>25</td>
      <td>56</td>
      <td>28</td>
      <td>70</td>
      <td>330</td>
      <td>40</td>
      <td>54</td>
    </tr>
    <tr>
      <th>30695</th>
      <td>USW00014739</td>
      <td>2020-01-15</td>
      <td>38</td>
      <td>111</td>
      <td>39</td>
      <td>280</td>
      <td>290</td>
      <td>81</td>
      <td>103</td>
    </tr>
    <tr>
      <th>30696</th>
      <td>USW00014739</td>
      <td>2020-01-16</td>
      <td>68</td>
      <td>83</td>
      <td>-10</td>
      <td>310</td>
      <td>320</td>
      <td>148</td>
      <td>201</td>
    </tr>
    <tr>
      <th>30697</th>
      <td>USW00014739</td>
      <td>2020-01-17</td>
      <td>90</td>
      <td>-10</td>
      <td>-88</td>
      <td>310</td>
      <td>320</td>
      <td>139</td>
      <td>188</td>
    </tr>
    <tr>
      <th>30698</th>
      <td>USW00014739</td>
      <td>2020-01-18</td>
      <td>39</td>
      <td>6</td>
      <td>-99</td>
      <td>320</td>
      <td>310</td>
      <td>89</td>
      <td>107</td>
    </tr>
    <tr>
      <th>30699</th>
      <td>USW00014739</td>
      <td>2020-01-19</td>
      <td>60</td>
      <td>72</td>
      <td>-43</td>
      <td>280</td>
      <td>260</td>
      <td>112</td>
      <td>148</td>
    </tr>
    <tr>
      <th>30700</th>
      <td>USW00014739</td>
      <td>2020-01-20</td>
      <td>62</td>
      <td>-10</td>
      <td>-71</td>
      <td>320</td>
      <td>330</td>
      <td>103</td>
      <td>134</td>
    </tr>
  </tbody>
</table>
</div>




```python
#date restrict Watertown1, and restrict the columns to station, date, precipitation, and snow
#remember this station did not have temperature or wind data
Watertown1=Watertown1[Watertown1['DATE']>='2020-01-01']
Watertown1=Watertown1[['STATION','DATE','PRCP','SNOW']]
```


```python
Watertown1.head(20) #precipitation is given in tenths of mm
```




<div>

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
      <th>599</th>
      <td>US1MAMD0119</td>
      <td>2020-01-01</td>
      <td>8</td>
      <td>0</td>
    </tr>
    <tr>
      <th>600</th>
      <td>US1MAMD0119</td>
      <td>2020-01-02</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>601</th>
      <td>US1MAMD0119</td>
      <td>2020-01-03</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>602</th>
      <td>US1MAMD0119</td>
      <td>2020-01-04</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>603</th>
      <td>US1MAMD0119</td>
      <td>2020-01-05</td>
      <td>43</td>
      <td>0</td>
    </tr>
    <tr>
      <th>604</th>
      <td>US1MAMD0119</td>
      <td>2020-01-06</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>605</th>
      <td>US1MAMD0119</td>
      <td>2020-01-07</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>606</th>
      <td>US1MAMD0119</td>
      <td>2020-01-08</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>607</th>
      <td>US1MAMD0119</td>
      <td>2020-01-09</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>608</th>
      <td>US1MAMD0119</td>
      <td>2020-01-10</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>609</th>
      <td>US1MAMD0119</td>
      <td>2020-01-11</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>610</th>
      <td>US1MAMD0119</td>
      <td>2020-01-12</td>
      <td>18</td>
      <td>0</td>
    </tr>
    <tr>
      <th>611</th>
      <td>US1MAMD0119</td>
      <td>2020-01-13</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>612</th>
      <td>US1MAMD0119</td>
      <td>2020-01-14</td>
      <td>5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>613</th>
      <td>US1MAMD0119</td>
      <td>2020-01-15</td>
      <td>3</td>
      <td>0</td>
    </tr>
    <tr>
      <th>614</th>
      <td>US1MAMD0119</td>
      <td>2020-01-16</td>
      <td>18</td>
      <td>0</td>
    </tr>
    <tr>
      <th>615</th>
      <td>US1MAMD0119</td>
      <td>2020-01-17</td>
      <td>15</td>
      <td>0</td>
    </tr>
    <tr>
      <th>616</th>
      <td>US1MAMD0119</td>
      <td>2020-01-18</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>617</th>
      <td>US1MAMD0119</td>
      <td>2020-01-19</td>
      <td>99</td>
      <td>86</td>
    </tr>
    <tr>
      <th>618</th>
      <td>US1MAMD0119</td>
      <td>2020-01-20</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



## Plotting Data

### Quick plots


```python
#first quick plot of the temperature in degrees Celsius (data given in tenths of degrees)
#seasons are clearly visible for the past couple years
days=np.arange(1,len(BostonLogan)+1)
plt.plot(days,BostonLogan['TMIN']/10)
plt.plot(days,BostonLogan['TMAX']/10);
```


    
![png](output_23_0.png)
    



```python
#first quick plot of precipitation/rain and snow in cm (data given in tenths of mm)
days=np.arange(1,len(Watertown1)+1)
plt.bar(days,Watertown1['PRCP']/100)
plt.bar(days,Watertown1['SNOW']/100);
```


    
![png](output_24_0.png)
    



```python
#first quick plot of wind speed in kilometers per hour (data is given in tenths of meters per second), 
#highlighting wind coming from ENE to ESE (60 to 120 degrees from true North) in CYAN
#use the speed and direction of fastest 2-min wind, as we have no hourly average data available
days=np.arange(1,len(BostonLogan)+1)
col=np.where((BostonLogan['WDF2']>=60) & (BostonLogan['WDF2']<=120),'c','k')
plt.scatter(days,BostonLogan['WSF2']*0.36,c=col,s=1); 
```


    
![png](output_25_0.png)
    


Next, create better plots that allow for color highlighting special conditions (such as wind coming from the ESE to ENE), with a proper scale on the x-axis (dates), and which properly connect relevant date ranges to special conditions.

### Detailed plots


```python
#indexing by date...this happens in-place
Watertown1.index=pd.DatetimeIndex(Watertown1.DATE)
BostonLogan.index=pd.DatetimeIndex(BostonLogan.DATE)
```


```python
#reindex, filling in missing dates with a row of NaNs
#so that both dataframes have the same index (NOW we have new objects so an assignment is necessary)
today=pd.to_datetime('today').date()
Watertown1=Watertown1.reindex(pd.date_range("2020-01-01", today))
BostonLogan=BostonLogan.reindex(pd.date_range("2020-01-01", today))
```


```python
Watertown1.head()
```




<div>

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
      <th>2020-01-01</th>
      <td>US1MAMD0119</td>
      <td>2020-01-01</td>
      <td>8</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2020-01-02</th>
      <td>US1MAMD0119</td>
      <td>2020-01-02</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2020-01-03</th>
      <td>US1MAMD0119</td>
      <td>2020-01-03</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2020-01-04</th>
      <td>US1MAMD0119</td>
      <td>2020-01-04</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2020-01-05</th>
      <td>US1MAMD0119</td>
      <td>2020-01-05</td>
      <td>43</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
BostonLogan.head()
```




<div>

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
      <th>2020-01-01</th>
      <td>USW00014739</td>
      <td>2020-01-01</td>
      <td>69</td>
      <td>61</td>
      <td>22</td>
      <td>260</td>
      <td>250</td>
      <td>130</td>
      <td>188</td>
    </tr>
    <tr>
      <th>2020-01-02</th>
      <td>USW00014739</td>
      <td>2020-01-02</td>
      <td>56</td>
      <td>94</td>
      <td>11</td>
      <td>280</td>
      <td>250</td>
      <td>94</td>
      <td>125</td>
    </tr>
    <tr>
      <th>2020-01-03</th>
      <td>USW00014739</td>
      <td>2020-01-03</td>
      <td>32</td>
      <td>111</td>
      <td>67</td>
      <td>230</td>
      <td>230</td>
      <td>76</td>
      <td>94</td>
    </tr>
    <tr>
      <th>2020-01-04</th>
      <td>USW00014739</td>
      <td>2020-01-04</td>
      <td>24</td>
      <td>89</td>
      <td>44</td>
      <td>350</td>
      <td>360</td>
      <td>63</td>
      <td>81</td>
    </tr>
    <tr>
      <th>2020-01-05</th>
      <td>USW00014739</td>
      <td>2020-01-05</td>
      <td>74</td>
      <td>50</td>
      <td>0</td>
      <td>310</td>
      <td>320</td>
      <td>139</td>
      <td>183</td>
    </tr>
  </tbody>
</table>
</div>




```python
BostonLogan.tail() #there appears to be a several day lag in publishing the latest data
```




<div>

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
      <th>2023-05-05</th>
      <td>USW00014739</td>
      <td>2023-05-05</td>
      <td>39</td>
      <td>128</td>
      <td>78</td>
      <td>40</td>
      <td>NaN</td>
      <td>67</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2023-05-06</th>
      <td>USW00014739</td>
      <td>2023-05-06</td>
      <td>NaN</td>
      <td>244</td>
      <td>106</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2023-05-07</th>
      <td>USW00014739</td>
      <td>2023-05-07</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2023-05-08</th>
      <td>NaN</td>
      <td>NaT</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2023-05-09</th>
      <td>NaN</td>
      <td>NaT</td>
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



Plot the precipitation (rain only) data for the year 2022 from Watertown1 dataframe, and pull the wind data from BostonLogan, highlight Eastern winds.


```python
plt.figure(figsize=(20,4.5))
plt.title('2022 Precipitation in Combination with strong Eastern winds in Watertown, MA')
days=pd.date_range("2022-01-01", "2022-12-31")
threshw=100 #wind threshold (tenths of meters per second)
threshr=100 #rain threshold (tenths of mm)
dirmin=60 #minimum wind direction (degrees from true North)
dirmax=140 #maximum wind direction
mask=((BostonLogan.loc[days]['WDF2']>=dirmin) & (BostonLogan.loc[days]['WDF2']<=dirmax) & (BostonLogan.loc[days]['WSF2']>=threshw)
      & (Watertown1.loc[days]['PRCP']>=threshr))
plt.bar(days, Watertown1.loc[days]['PRCP'])
plt.scatter(days[mask],Watertown1.loc[days].loc[mask]['PRCP'],marker='o')
plt.axis(xmin=days[0].date(),xmax=days[-1].date())
plt.ylabel('Precipitation [1/10 mm]')
plt.xticks(days[mask],rotation=90);
```


    
![png](output_34_0.png)
    



```python
BostonLogan.loc[days].loc[mask][['AWND','WSF2']]
#and the average wind speed vs fastest 2-min wind (WSF2) may give us an
#idea about which days really had sustained strong Eastern winds
#even better: obtain more granular data (hourly)
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AWND</th>
      <th>WSF2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2022-01-17</th>
      <td>107</td>
      <td>197</td>
    </tr>
    <tr>
      <th>2022-03-24</th>
      <td>75</td>
      <td>107</td>
    </tr>
    <tr>
      <th>2022-04-08</th>
      <td>55</td>
      <td>134</td>
    </tr>
    <tr>
      <th>2022-04-19</th>
      <td>97</td>
      <td>165</td>
    </tr>
    <tr>
      <th>2022-10-14</th>
      <td>44</td>
      <td>125</td>
    </tr>
    <tr>
      <th>2022-11-16</th>
      <td>67</td>
      <td>116</td>
    </tr>
    <tr>
      <th>2022-12-16</th>
      <td>110</td>
      <td>143</td>
    </tr>
  </tbody>
</table>
</div>




```python
#create plotting function..this can also be found in getweatherdata.py
def make_labeled_plot(title):
    fig,ax=plt.subplots(figsize=(20,4.5))
    ax.set_title(title)
    plt.setp(ax.get_xticklabels(),rotation=90)
    return fig,ax
```


```python
#plot update function...adapt for other locations
def barplot_weather(ax,year,threshr,threshw,direction,complement):
    #check if any changes to the bar heights and xlim are necessary (i.e., check if xlim is already set/correct)
    if year!=str(num2date(ax.get_xlim()[0]).date().year):
        #set view x-limits for current year
        if pd.to_datetime(year+'-12-31')>BostonLogan.index[-1]:
            dates=pd.date_range(year+'-01-01',BostonLogan.index[-1])
        else:
            dates=pd.date_range(year+'-01-01',year+'-12-31')    
        ax.set_xlim(xmin=dates[0].date(),xmax=dates[-1].date())  
        if len(ax.containers)>0: #already have bars (drawn)
            ax.containers[0].remove() #this works, whereas .pop() does not remove the already drawn artist
                                      #from the canvas, so it comes into view again when xlim is set appropriately
        ax.bar(Watertown1.loc[dates].index,Watertown1.loc[dates]['PRCP'])#this (re-)creates the barplot artist in ax
        #need the prior call to .remove(), as every call to ax.bar()
        #adds a new barcontainer artist to ax.containers, which is not what we want;
        #to avoid adding and removing the same bar plots repeatedly, would need to make
        #bar plot of all data (2020-2023) and edit the opacity of the correct portion (within current xlim)
    else: #year hasn't changed
        xlims=ax.get_xlim()
        dates=pd.date_range(num2date(xlims[0]).date(),num2date(xlims[1]).date()) 
    mask= (BostonLogan.loc[dates]['WSF2']>=threshw) & (Watertown1.loc[dates]['PRCP']>=threshr)
    if complement:
        mask=mask&((BostonLogan.loc[dates]['WDF2']<=direction[0]) | (BostonLogan.loc[dates]['WDF2']>=direction[1]))
    else:
        mask=mask&(BostonLogan.loc[dates]['WDF2']>=direction[0]) & (BostonLogan.loc[dates]['WDF2']<=direction[1])
    bars=ax.containers[0]
    for i in range(len(bars)): #update the bars with color and opacity according to mask
        if mask[i]:
            bars[i].set(color='r',alpha=1)
        else:
            bars[i].set(color='k',alpha=0.3)
    ticks=ax.set_xticks(BostonLogan.loc[dates].loc[mask].index)
```


```python
#%matplotlib notebook
#uncomment the above to have interactive output (functional sliders, etc.) for this cell
#or simply run the following cell for an alternative using ipywidgets

#initialize plot
fig,ax=make_labeled_plot('Precipitation and Wind in Watertown, MA')

#set y limits and labels
ax.set_ylim(bottom=0,top=max(Watertown1['PRCP']))
ax.set_ylabel('Precipitation [1/10 mm]')

#initial values and ranges for controls
dirmin_init=60
dirmax_init=140
rrange=[0,max(Watertown1['PRCP'])]
threshr_init=100
wrange=[0,400]
threshw_init=100
years=['2020','2021','2022','2023']
year_init='2022'

#make room for the controls
fig.subplots_adjust(left=0.1, bottom=0.5)

#create new axes, radio buttons, sliders, and checkbox
axr=fig.add_axes([0.04, 0.5, 0.01, 0.38])
r_slider=Slider(ax=axr,valinit=threshr_init,valmin=rrange[0],valmax=rrange[1],label='rain threshold',orientation='vertical')
axy=fig.add_axes([0.11, 0.1, 0.1, 0.15])
y_buttons=RadioButtons(ax=axy,labels=years, active=years.index(year_init))
axw=fig.add_axes([0.35, 0.2, 0.2, 0.04])
w_slider=Slider(ax=axw,valinit=threshw_init,valmin=wrange[0],valmax=wrange[1],label='wind threshold')
axd=fig.add_axes([0.35, 0.1, 0.2, 0.04])
d_slider=RangeSlider(ax=axd,valinit=[dirmin_init,dirmax_init],valmin=0,valmax=360,label='wind direction')
axc=fig.add_axes([0.63, 0.1, 0.27, 0.04])
c_box=CheckButtons(ax=axc,labels=['use complement of direction interval'])

#update function accepts exactly one (dummy) argument
def update(arg):
    #vals of radio buttons, sliders and the status of the first (and only)
    #checkbutton passed to the actual update function barplot_weather()
    barplot_weather(ax,y_buttons.value_selected,r_slider.val,w_slider.val,d_slider.val,c_box.get_status()[0]) 
    #fig.canvas.draw_idle() ... not necesssary within jupyter notebook
#register sliders and checkbox with the update function
y_buttons.on_clicked(update)
r_slider.on_changed(update)
w_slider.on_changed(update)
d_slider.on_changed(update)
c_box.on_clicked(update)
update(0); #for initial plot before any controls are changed
#plt.show() ... not necessary within jupyter notebook
```


    
![png](output_38_0.png)
    



```python
#%matplotlib inline
#run the notebook in order to use the widgets and see the output
fig2,ax2=make_labeled_plot('Precipitation and Wind in Watertown, MA')

plt.close(fig2) #don't show figure (yet), stops first (empty) plot from appearing

#set y limits and labels
ax2.set_ylim(bottom=0,top=max(Watertown1['PRCP']))
ax2.set_ylabel('Precipitation [1/10 mm]')

#initial values and ranges for controls
dirmin_init=60
dirmax_init=140
rrange=[0,max(Watertown1['PRCP'])]
threshr_init=100
wrange=[0,400]
threshw_init=100
years=['2020','2021','2022','2023']
year_init='2022'

#plot update function
def update_interact(year,threshr,threshw,direction,complement):
    barplot_weather(ax2,year,threshr,threshw,direction,complement)
    #neither plt.show() nor fig.canvas.draw_idle() seem to actually update the plot
    display(fig2)#this or "return fig2" is needed, completely redraws the figure below
                 #but it doesn't close/update fig if drawn outside of this function
                 #plt.clf() also does not remove fig if drawn outside of this function
      
y_menu=widgets.Dropdown(options=years,value=year_init,description='year')
r_slider=widgets.IntSlider(value=threshr_init,min=rrange[0],max=rrange[1],step=1, description='rain threshold', continuous_update=False)
w_slider=widgets.IntSlider(value=threshw_init,min=wrange[0],max=wrange[1],step=1,description='wind threshold', continuous_update=False)
d_slider=widgets.IntRangeSlider(value=[dirmin_init,dirmax_init],min=0,max=360,step=1,description='wind direction', continuous_update=False)
c_box=widgets.Checkbox(value=False,description='use complement of direction interval',disabled=False,indent=False)


interact(update_interact,year=y_menu,threshr=r_slider,threshw=w_slider,direction=d_slider,complement=c_box);

```


    interactive(children=(Dropdown(description='year', index=2, options=('2020', '2021', '2022', '2023'), value='2…



```python

```
