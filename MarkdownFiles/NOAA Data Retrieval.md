```python
import requests
import os
import numpy as np
import pandas as pd
```

The NOAA publishes historical weather data. Details can be found in the [readme](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt). In this notebook, we explore how to quickly download data in a format similar to what can be ordered through their  search tool [Climate Data Online](https://www.ncei.noaa.gov/cdo-web/) (which can sometimes take days to send a download link).


```python
response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt') #stations in the network
```


```python
response.status_code #it worked!
```




    200




```python
response.url
```




    'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt'




```python
with open('stationdata.txt', 'w') as file: #write stations to file for future reference
    file.write(response.text) #or use response.content in mode 'wb'
```


```python
#from readme
#IV. FORMAT OF "ghcnd-stations.txt"

#------------------------------
#Variable   Columns   Type
#------------------------------
#ID            1-11   Character
#LATITUDE     13-20   Real
#LONGITUDE    22-30   Real
#ELEVATION    32-37   Real
#STATE        39-40   Character
#NAME         42-71   Character
#GSN FLAG     73-75   Character
#HCN/CRN FLAG 77-79   Character
#WMO ID       81-85   Character
#------------------------------
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

We can now pick stations for which to download historical weather data. In this example, we download data from the nearest station for Watertown, MA.


```python
stations[stations['name']=='WATERTOWN'] #this only shows Watertown, MN and Watertown, NY
```




    array([('USC00218713', 44.9667, -93.85  , -999.9, 'MN', 'WATERTOWN', '', '', ''),
           ('USC00309000', 43.9761, -75.8753,  151.5, 'NY', 'WATERTOWN', '', 'HCN', '')],
          dtype=[('id', '<U11'), ('latitude', '<f8'), ('longitude', '<f8'), ('elevation', '<f8'), ('state', '<U3'), ('name', '<U31'), ('gsn', '<U4'), ('hcn', '<U4'), ('wmo', '<U6')])




```python
stations[np.char.find(stations['name'],'WATERTOWN')==0] #any other stations beginning with 'WATERTOWN'?
```




    array([('US1CTLT0010', 41.5995, -73.1378,  245.7, 'CT', 'WATERTOWN 1.1 WSW', '', '', ''),
           ('US1CTLT0014', 41.5991, -73.1166,  178.9, 'CT', 'WATERTOWN 0.5 S', '', '', ''),
           ('US1CTLT0046', 41.654 , -73.1228,  217.9, 'CT', 'WATERTOWN 3.4 N', '', '', ''),
           ('US1MAMD0119', 42.3711, -71.1995,   16.5, 'MA', 'WATERTOWN 1.1 W', '', '', ''),
           ('US1MAMD0186', 42.3786, -71.1959,   36. , 'MA', 'WATERTOWN 1.1 NW', '', '', ''),
           ('US1MNCV0008', 44.9663, -93.8489,  295.7, 'MN', 'WATERTOWN 0.5 NNW', '', '', ''),
           ('US1NYJF0010', 43.9819, -75.934 ,  122.2, 'NY', 'WATERTOWN 1.3 WNW', '', '', ''),
           ('US1NYJF0020', 43.9708, -75.909 ,  151.8, 'NY', 'WATERTOWN 0.2 SSE', '', '', ''),
           ('US1NYJF0032', 43.9669, -75.892 ,  159.1, 'NY', 'WATERTOWN 1.0 ESE', '', '', ''),
           ('US1NYJF0044', 44.0743, -75.9235,  115.2, 'NY', 'WATERTOWN 7.0 N', '', '', ''),
           ('US1SDCD0001', 44.959 , -97.0247,  580. , 'SD', 'WATERTOWN 7.6 ENE', '', '', ''),
           ('US1SDCD0002', 44.9429, -97.1461,  526.1, 'SD', 'WATERTOWN 2.3 NNE', '', '', ''),
           ('US1SDCD0005', 45.0043, -97.0857,  542.8, 'SD', 'WATERTOWN 7.5 NNE', '', '', ''),
           ('US1SDCD0008', 44.9074, -97.1116,  534.3, 'SD', 'WATERTOWN 2.7 E', '', '', ''),
           ('US1SDCD0009', 44.928 , -97.1732,  531. , 'SD', 'WATERTOWN 1.1 NNW', '', '', ''),
           ('US1SDCD0010', 44.9207, -97.2299,  527.3, 'SD', 'WATERTOWN 3.1 W', '', '', ''),
           ('US1SDCD0011', 44.8971, -97.2481,  525.8, 'SD', 'WATERTOWN 4.1 WSW', '', '', ''),
           ('US1SDCD0014', 44.9091, -97.1141,  541.3, 'SD', 'WATERTOWN 2.6 E', '', '', ''),
           ('US1SDCD0015', 44.9373, -97.0837,  550.2, 'SD', 'WATERTOWN 4.4 ENE', '', '', ''),
           ('US1SDCD0018', 44.909 , -97.2122,  525.5, 'SD', 'WATERTOWN 2.2 W', '', '', ''),
           ('US1SDCD0021', 44.9158, -97.0915,  544.1, 'SD', 'WATERTOWN 3.7 E', '', '', ''),
           ('US1SDCD0025', 44.9468, -97.2565,  545. , 'SD', 'WATERTOWN 5.0 WNW', '', '', ''),
           ('US1SDCD0026', 44.8192, -97.2058,  550.5, 'SD', 'WATERTOWN 6.7 SSW', '', '', ''),
           ('US1SDCD0030', 44.916 , -97.1192,  545.6, 'SD', 'WATERTOWN 2.3 E', '', '', ''),
           ('US1SDCD0032', 44.918 , -97.1178,  548.9, 'SD', 'WATERTOWN 2.4 E', '', '', ''),
           ('US1TNWN0021', 36.0355, -86.1974,  262.1, 'TN', 'WATERTOWN 5.5 SW', '', '', ''),
           ('US1WIDD0022', 43.2067, -88.7145,  256.3, 'WI', 'WATERTOWN 1.2 NNE', '', '', ''),
           ('US1WIJF0002', 43.1792, -88.6972,  253. , 'WI', 'WATERTOWN 1.6 ESE', '', '', ''),
           ('US1WIJF0004', 43.1761, -88.7286,  247.8, 'WI', 'WATERTOWN 1.1 S', '', '', ''),
           ('US1WIJF0019', 43.1806, -88.724 ,  254.8, 'WI', 'WATERTOWN 0.8 S', '', '', ''),
           ('USC00218713', 44.9667, -93.85  , -999.9, 'MN', 'WATERTOWN', '', '', ''),
           ('USC00309000', 43.9761, -75.8753,  151.5, 'NY', 'WATERTOWN', '', 'HCN', ''),
           ('USC00398930', 44.9028, -97.1136,  533.4, 'SD', 'WATERTOWN 1W', '', '', ''),
           ('USC00398931', 44.9075, -97.1153,  538.9, 'SD', 'WATERTOWN COOP', '', '', ''),
           ('USC00409481', 36.0967, -86.1397,  196.6, 'TN', 'WATERTOWN PUBLIC SAFETY COMPLE', '', '', ''),
           ('USC00478919', 43.1742, -88.7364,  251.5, 'WI', 'WATERTOWN WWTP', '', 'HCN', ''),
           ('USW00014946', 44.9044, -97.1494,  530.7, 'SD', 'WATERTOWN RGNL AP', '', 'HCN', ''),
           ('USW00094790', 43.9886, -76.0261,   94.8, 'NY', 'WATERTOWN AP', '', '', '')],
          dtype=[('id', '<U11'), ('latitude', '<f8'), ('longitude', '<f8'), ('elevation', '<f8'), ('state', '<U3'), ('name', '<U31'), ('gsn', '<U4'), ('hcn', '<U4'), ('wmo', '<U6')])



There are two stations in Watertown, MA, US1MAMD0119 and US1MAMD0186. They have no GSN, HCN, or WMO network id, so they may only have limited data available. Proceed to download the data for the first station to a file.


```python
response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/US1MAMD0119.dly')
with open('WATERTOWN.dly', 'w') as file:
    file.write(response.text) #or use response.content in mode 'wb'
```


```python
#format from readme

#------------------------------
#Variable   Columns   Type
#------------------------------
#ID            1-11   Character
#YEAR         12-15   Integer
#MONTH        16-17   Integer
#ELEMENT      18-21   Character
#VALUE1       22-26   Integer
#MFLAG1       27-27   Character
#QFLAG1       28-28   Character
#SFLAG1       29-29   Character
#VALUE2       30-34   Integer
#MFLAG2       35-35   Character
#QFLAG2       36-36   Character
#SFLAG2       37-37   Character
#  .           .          .
#  .           .          .
#  .           .          .
#VALUE31    262-266   Integer
#MFLAG31    267-267   Character
#QFLAG31    268-268   Character
#SFLAG31    269-269   Character
#------------------------------

#These variables have the following definitions:
#
#ID         is the station identification code.  Please see "ghcnd-stations.txt"
#           for a complete list of stations and their metadata.
#YEAR       is the year of the record.
#
#MONTH      is the month of the record.
#
#ELEMENT    is the element type.   There are five core elements as well as a number
#           of addition elements.  
#   
#   The five core elements are:
#
#   PRCP = Precipitation (tenths of mm)
#   SNOW = Snowfall (mm)
#   SNWD = Snow depth (mm)
#   TMAX = Maximum temperature (tenths of degrees C)
#   TMIN = Minimum temperature (tenths of degrees C)


#   WESD = Water equivalent of snow on the ground (tenths of mm)
#   WESF = Water equivalent of snowfall (tenths of mm)

#... and so on through the 31st day of the month.  Note: If the month has less 
#than 31 days, then the remaining variables are set to missing (e.g., for April, 
#VALUE31 = -9999, MFLAG31 = blank, QFLAG31 = blank, SFLAG31 = blank).

```

To work with the data, it is useful to read the file into a pandas DataFrame. Note that the .dly-file does not contain further information about the station itself other than its id.


```python
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
```


```python
pdata=dly_to_df('WATERTOWN.dly') #this station only provides precipitation data, no temperature data
pdata
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
      <th>YEAR</th>
      <th>MONTH</th>
      <th>ELEMENT</th>
      <th>day1</th>
      <th>m1</th>
      <th>q1</th>
      <th>s1</th>
      <th>day2</th>
      <th>m2</th>
      <th>...</th>
      <th>q29</th>
      <th>s29</th>
      <th>day30</th>
      <th>m30</th>
      <th>q30</th>
      <th>s30</th>
      <th>day31</th>
      <th>m31</th>
      <th>q31</th>
      <th>s31</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>PRCP</td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
    <tr>
      <th>1</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>SNOW</td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
    <tr>
      <th>2</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>SNWD</td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
    <tr>
      <th>3</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>WESD</td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
    <tr>
      <th>4</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>WESF</td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>300</th>
      <td>US1MAMD0119</td>
      <td>2023</td>
      <td>5</td>
      <td>PRCP</td>
      <td>330.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>3.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>301</th>
      <td>US1MAMD0119</td>
      <td>2023</td>
      <td>5</td>
      <td>SNOW</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>302</th>
      <td>US1MAMD0119</td>
      <td>2023</td>
      <td>5</td>
      <td>SNWD</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>303</th>
      <td>US1MAMD0119</td>
      <td>2023</td>
      <td>5</td>
      <td>WESD</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>304</th>
      <td>US1MAMD0119</td>
      <td>2023</td>
      <td>5</td>
      <td>WESF</td>
      <td>0.0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>0.0</td>
      <td></td>
      <td>...</td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9999.0</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>305 rows × 128 columns</p>
</div>



We now reformat this data frame step by step, so that each day of data shows up in a separate row, with each element a column, and each set of element attributes another column.


```python
pdata = pd.melt(pdata, id_vars=['STATION','YEAR','MONTH','ELEMENT']) #first convert to long format
pdata.head()
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
      <th>YEAR</th>
      <th>MONTH</th>
      <th>ELEMENT</th>
      <th>variable</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>PRCP</td>
      <td>day1</td>
      <td>-9999</td>
    </tr>
    <tr>
      <th>1</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>SNOW</td>
      <td>day1</td>
      <td>-9999</td>
    </tr>
    <tr>
      <th>2</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>SNWD</td>
      <td>day1</td>
      <td>-9999</td>
    </tr>
    <tr>
      <th>3</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>WESD</td>
      <td>day1</td>
      <td>-9999</td>
    </tr>
    <tr>
      <th>4</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>WESF</td>
      <td>day1</td>
      <td>-9999</td>
    </tr>
  </tbody>
</table>
</div>




```python
pdata['DAY']=pdata['variable'].apply(lambda x: int(x[3:]) if len(x)>3 else int(x[1:])) #create a separate variable 'DAY'
```


```python
pdata['variable']=pdata['variable'].apply(lambda x: x[:3] if len(x)>3 else x[0]) #and reduce the 'variable' column to 'day'
#or flag identifiers 'm', 'q', 's'
```


```python
pdata.head()
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
      <th>YEAR</th>
      <th>MONTH</th>
      <th>ELEMENT</th>
      <th>variable</th>
      <th>value</th>
      <th>DAY</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>PRCP</td>
      <td>day</td>
      <td>-9999</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>SNOW</td>
      <td>day</td>
      <td>-9999</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>SNWD</td>
      <td>day</td>
      <td>-9999</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>WESD</td>
      <td>day</td>
      <td>-9999</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>WESF</td>
      <td>day</td>
      <td>-9999</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
#every date for every element has 'variable' entries 'day', 'm','q','s'
#use 'STATION','YEAR','MONTH','DAY','ELEMENT' as row index and the entries in 'variable' to create new columns with values
#associated from the 'value' column
pdata=pd.pivot(pdata,index=['STATION','YEAR','MONTH','DAY','ELEMENT'],columns=['variable'], values='value')
pdata.head()
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
      <th></th>
      <th></th>
      <th></th>
      <th>variable</th>
      <th>day</th>
      <th>m</th>
      <th>q</th>
      <th>s</th>
    </tr>
    <tr>
      <th>STATION</th>
      <th>YEAR</th>
      <th>MONTH</th>
      <th>DAY</th>
      <th>ELEMENT</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">US1MAMD0119</th>
      <th rowspan="5" valign="top">2018</th>
      <th rowspan="5" valign="top">5</th>
      <th rowspan="5" valign="top">1</th>
      <th>PRCP</th>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>SNOW</th>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>SNWD</th>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>WESD</th>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>WESF</th>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
pdata.rename(columns={'day':'value'}, inplace=True)
pdata.columns
```




    Index(['value', 'm', 'q', 's'], dtype='object', name='variable')




```python
pdata.reset_index(inplace=True) #simple index for each row, with 'STATION', 'YEAR','MONTH','DAY','ELEMENT' columns
pdata.head()
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
      <th>variable</th>
      <th>STATION</th>
      <th>YEAR</th>
      <th>MONTH</th>
      <th>DAY</th>
      <th>ELEMENT</th>
      <th>value</th>
      <th>m</th>
      <th>q</th>
      <th>s</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>1</td>
      <td>PRCP</td>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>1</td>
      <td>SNOW</td>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>1</td>
      <td>SNWD</td>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>1</td>
      <td>WESD</td>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>1</td>
      <td>WESF</td>
      <td>-9999</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
#throw out data for all days with 'invalid' values
pdata = pdata[pdata.value != -9999]
#such days are, e.g., Feb 30
```


```python
# make a column 'DATE' out of year, month, day
pdata['DATE'] = pd.to_datetime(pdata[['YEAR','MONTH','DAY']])
pdata.head()
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
      <th>variable</th>
      <th>STATION</th>
      <th>YEAR</th>
      <th>MONTH</th>
      <th>DAY</th>
      <th>ELEMENT</th>
      <th>value</th>
      <th>m</th>
      <th>q</th>
      <th>s</th>
      <th>DATE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>PRCP</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
    <tr>
      <th>11</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>SNOW</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
    <tr>
      <th>12</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>SNWD</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
    <tr>
      <th>13</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>WESD</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
    <tr>
      <th>14</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>WESF</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
  </tbody>
</table>
</div>




```python
pdata.columns.name=None #the identifier 'variable' for the column names is not needed
pdata.head()
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
      <th>YEAR</th>
      <th>MONTH</th>
      <th>DAY</th>
      <th>ELEMENT</th>
      <th>value</th>
      <th>m</th>
      <th>q</th>
      <th>s</th>
      <th>DATE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>PRCP</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
    <tr>
      <th>11</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>SNOW</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
    <tr>
      <th>12</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>SNWD</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
    <tr>
      <th>13</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>WESD</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
    <tr>
      <th>14</th>
      <td>US1MAMD0119</td>
      <td>2018</td>
      <td>5</td>
      <td>3</td>
      <td>WESF</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>2018-05-03</td>
    </tr>
  </tbody>
</table>
</div>




```python
#forget separate YEAR,MONTH,DAY columns
pdata=pdata[['STATION','DATE','ELEMENT','value','m','q','s']]
pdata.head()
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
      <th>ELEMENT</th>
      <th>value</th>
      <th>m</th>
      <th>q</th>
      <th>s</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>PRCP</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
    <tr>
      <th>11</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>SNOW</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
    <tr>
      <th>12</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>SNWD</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
    <tr>
      <th>13</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>WESD</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
    <tr>
      <th>14</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>WESF</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
    </tr>
  </tbody>
</table>
</div>




```python
#consolidate the flags for each element in an 'ATTRIBUTES' column
pdata['ATTRIBUTES']=pdata['m']+','+pdata['q']+','+pdata['s']
pdata.head()
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
      <th>ELEMENT</th>
      <th>value</th>
      <th>m</th>
      <th>q</th>
      <th>s</th>
      <th>ATTRIBUTES</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>PRCP</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>11</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>SNOW</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>12</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>SNWD</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>13</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>WESD</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>14</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>WESF</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>N</td>
      <td>,,N</td>
    </tr>
  </tbody>
</table>
</div>




```python
#forget separate m, q, s columns
pdata=pdata[['STATION','DATE','ELEMENT','value','ATTRIBUTES']]
pdata.head()
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
      <th>ELEMENT</th>
      <th>value</th>
      <th>ATTRIBUTES</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>PRCP</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>11</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>SNOW</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>12</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>SNWD</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>13</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>WESD</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>14</th>
      <td>US1MAMD0119</td>
      <td>2018-05-03</td>
      <td>WESF</td>
      <td>0</td>
      <td>,,N</td>
    </tr>
  </tbody>
</table>
</div>




```python
#now, for each day, get all elements and attributes to show up in a row
pdata = pdata.pivot(index=['STATION','DATE'], columns='ELEMENT')
pdata.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th colspan="5" halign="left">value</th>
      <th colspan="5" halign="left">ATTRIBUTES</th>
    </tr>
    <tr>
      <th></th>
      <th>ELEMENT</th>
      <th>PRCP</th>
      <th>SNOW</th>
      <th>SNWD</th>
      <th>WESD</th>
      <th>WESF</th>
      <th>PRCP</th>
      <th>SNOW</th>
      <th>SNWD</th>
      <th>WESD</th>
      <th>WESF</th>
    </tr>
    <tr>
      <th>STATION</th>
      <th>DATE</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">US1MAMD0119</th>
      <th>2018-05-03</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>2018-05-04</th>
      <td>13</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>2018-05-05</th>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>2018-05-06</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>T,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
    </tr>
    <tr>
      <th>2018-05-07</th>
      <td>71</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
      <td>,,N</td>
    </tr>
  </tbody>
</table>
</div>




```python
pdata.columns
```




    MultiIndex([(     'value', 'PRCP'),
                (     'value', 'SNOW'),
                (     'value', 'SNWD'),
                (     'value', 'WESD'),
                (     'value', 'WESF'),
                ('ATTRIBUTES', 'PRCP'),
                ('ATTRIBUTES', 'SNOW'),
                ('ATTRIBUTES', 'SNWD'),
                ('ATTRIBUTES', 'WESD'),
                ('ATTRIBUTES', 'WESF')],
               names=[None, 'ELEMENT'])




```python
#rename the columns
pdata.rename(columns={'value':''}, inplace=True)
pdata.columns
```




    MultiIndex([(          '', 'PRCP'),
                (          '', 'SNOW'),
                (          '', 'SNWD'),
                (          '', 'WESD'),
                (          '', 'WESF'),
                ('ATTRIBUTES', 'PRCP'),
                ('ATTRIBUTES', 'SNOW'),
                ('ATTRIBUTES', 'SNWD'),
                ('ATTRIBUTES', 'WESD'),
                ('ATTRIBUTES', 'WESF')],
               names=[None, 'ELEMENT'])




```python
pdata.columns = ['_'.join(col).rstrip('_') for col in [c[::-1] for c in pdata.columns.values]]
pdata.columns
```




    Index(['PRCP', 'SNOW', 'SNWD', 'WESD', 'WESF', 'PRCP_ATTRIBUTES',
           'SNOW_ATTRIBUTES', 'SNWD_ATTRIBUTES', 'WESD_ATTRIBUTES',
           'WESF_ATTRIBUTES'],
          dtype='object')




```python
#alphabetical order of columns
pdata=pdata[list(pdata.columns.sort_values())]
pdata.head()
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
      <th></th>
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
    <tr>
      <th>STATION</th>
      <th>DATE</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="5" valign="top">US1MAMD0119</th>
      <th>2018-05-03</th>
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
      <th>2018-05-04</th>
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
      <th>2018-05-05</th>
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
      <th>2018-05-06</th>
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
      <th>2018-05-07</th>
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
pdata.reset_index(inplace=True)
pdata.head()
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
pdata.to_csv('WATERTOWN.csv',index=False) #save to .csv
```


```python
#create a function aggregating all these steps
def dly_to_csv(filename, target=None):
    # load the fixed-width file following the format in readme.txt
    # and label the columns
    pdata=dly_to_df(filename) #convert to pandas DataFrame
    
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
    return pdata
```


```python
Watertown=dly_to_csv('WATERTOWN.dly','WATERTOWN')
Watertown.head()
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



For comparison, let us try a station that has more data, because it is in the GSN ([GCOS surface network](https://gcos.wmo.int/en/networks/atmospheric/gsn)), HCN (Historical Climatology Network), or WMO (World Meteorological Organization) network of stations.


```python
stations[np.char.find(stations['name'],'BOSTON')==0] #search for stations beginning with 'BOSTON'
```




    array([('ASN00064019', -32.2833,  149.0833, -999.9, '', 'BOSTON (GOLLAN)', '', '', ''),
           ('CA00111090M',  49.8667, -121.4333,  200. , 'BC', 'BOSTON BAR', '', '', ''),
           ('CA001110R04',  49.8667, -121.45  ,  163. , 'BC', 'BOSTON BAR', '', '', ''),
           ('CA1BC000018',  49.88  , -121.4533,  164.9, 'BC', 'BOSTON BAR 2.1 NNW', '', '', ''),
           ('CA1ON000066',  42.9851,  -80.268 ,  236.5, 'ON', 'BOSTON 0.8 SSE', '', '', ''),
           ('US1GATH0005',  30.8403,  -83.8033,   59.7, 'GA', 'BOSTON 3.4 NNW', '', '', ''),
           ('US1MASF0001',  42.357 ,  -71.0671,   13.1, 'MA', 'BOSTON 0.5 WSW', '', '', ''),
           ('US1MASF0031',  42.2927,  -71.1456,   54.6, 'MA', 'BOSTON 6.5 SW', '', '', ''),
           ('US1NYER0065',  42.6547,  -78.7201,  475.8, 'NY', 'BOSTON 1.5 NE', '', '', ''),
           ('US1NYER0166',  42.6548,  -78.703 ,  490.7, 'NY', 'BOSTON 2.5 NE', '', '', ''),
           ('US1VARP0006',  38.5339,  -78.1741,  175.3, 'VA', 'BOSTON 2.2 WSW', '', '', ''),
           ('USC00150874',  37.7667,  -85.7   ,  146. , 'KY', 'BOSTON 2 SW', '', '', ''),
           ('USC00150875',  37.7436,  -85.7483,  259.1, 'KY', 'BOSTON 6 SW', '', '', ''),
           ('USC00190768',  42.35  ,  -71.0667,    5.2, 'MA', 'BOSTON', '', '', ''),
           ('USC00440860',  38.5458,  -78.0981,  179.8, 'VA', 'BOSTON 4 SE', '', '', ''),
           ('USW00014739',  42.3606,  -71.0097,    3.4, 'MA', 'BOSTON', '', '', '72509'),
           ('USW00094701',  42.35  ,  -71.0667,    6.1, 'MA', 'BOSTON CITY WSO', '', '', '')],
          dtype=[('id', '<U11'), ('latitude', '<f8'), ('longitude', '<f8'), ('elevation', '<f8'), ('state', '<U3'), ('name', '<U31'), ('gsn', '<U4'), ('hcn', '<U4'), ('wmo', '<U6')])



We see there is one station at Boston Logan International Airport in Boston, MA that is in the WMO network.


```python
response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00014739.dly')
with open('BOSTON.dly', 'w') as file:
    file.write(response.text)
```


```python
Boston=dly_to_csv('BOSTON.dly','BOSTON')
```


```python
#look at the column names present and select a list of those starting with P,S,T and second letter R,S,M
cols=list(Boston.columns.values)
mask=list(pd.Series(cols).str.match('[PST][RNM]'))
cols=[col for i,col in enumerate(cols) if mask[i]]
```


```python
cols #this picks out the most common elements and their attributes
```




    ['PRCP',
     'PRCP_ATTRIBUTES',
     'SNOW',
     'SNOW_ATTRIBUTES',
     'SNWD',
     'SNWD_ATTRIBUTES',
     'TMAX',
     'TMAX_ATTRIBUTES',
     'TMIN',
     'TMIN_ATTRIBUTES']




```python
Boston=Boston[['STATION','DATE']+cols]
#select dates from May 2018 where the above data for Watertown starts
Boston=Boston[Boston['DATE']>='2018-05-03']
Boston.head()
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
      <th>TMAX</th>
      <th>TMAX_ATTRIBUTES</th>
      <th>TMIN</th>
      <th>TMIN_ATTRIBUTES</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>30073</th>
      <td>USW00014739</td>
      <td>2018-05-03</td>
      <td>23</td>
      <td>,,W</td>
      <td>0</td>
      <td>,,W</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>322</td>
      <td>,,W</td>
      <td>161</td>
      <td>,,W</td>
    </tr>
    <tr>
      <th>30074</th>
      <td>USW00014739</td>
      <td>2018-05-04</td>
      <td>0</td>
      <td>T,,W</td>
      <td>0</td>
      <td>,,W</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>278</td>
      <td>,,W</td>
      <td>139</td>
      <td>,,W</td>
    </tr>
    <tr>
      <th>30075</th>
      <td>USW00014739</td>
      <td>2018-05-05</td>
      <td>0</td>
      <td>,,W</td>
      <td>0</td>
      <td>,,W</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>239</td>
      <td>,,W</td>
      <td>144</td>
      <td>,,W</td>
    </tr>
    <tr>
      <th>30076</th>
      <td>USW00014739</td>
      <td>2018-05-06</td>
      <td>48</td>
      <td>,,W</td>
      <td>0</td>
      <td>,,W</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>194</td>
      <td>,,W</td>
      <td>100</td>
      <td>,,W</td>
    </tr>
    <tr>
      <th>30077</th>
      <td>USW00014739</td>
      <td>2018-05-07</td>
      <td>0</td>
      <td>,,W</td>
      <td>0</td>
      <td>,,W</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>161</td>
      <td>,,W</td>
      <td>89</td>
      <td>,,W</td>
    </tr>
  </tbody>
</table>
</div>



When working with the data, we may have to reformat some 'ELEMENT' columns. Refer to the [documentation](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) to find the exact units (such as tenths of degrees Celsius, tenths of mm,...) and convert them to the units of your liking (e.g. degrees Fahrenheit, inches, mm).

Final note: For an individual station, it is also possible to retrieve a corresponding '.csv.gz' file from the NOAA at https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/. Apart from being gzip-files, the contained .csv-files also follow a different format, with each single record being an observation of some element, and its flags, on a specific day. See [here](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/readme-by_station.txt).
