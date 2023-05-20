import requests
import os
import numpy as np
import pandas as pd
import weatherdata as w
import matplotlib.pyplot as plt

while True: #main loop...
    city=input('City (hit ENTER for default=Boston): ')

    state=input('State or Province (hit ENTER for default=MA): ')
    if city=='':
        city='Boston'
    if state=='':
        state='MA' #so this does not allow searches for locations outside US/Canada
                   #because the state will default to 'MA' if empty
    stations = w.get_stations(city,state)
    n=len(stations)
    if n==0:
        print('No stations found for {city}, {state}.')
    else:
        print(f'Stations found for {city}, {state}: ')
        print('Option \t Station')
        for i,station in enumerate(stations):
            print(i+1,'\t',station)
        while True: #keep asking for input until a valid number or 'q' is entered
            selection=input(f'Select option from list above (1-{n}) or press \'q\'(quit): ')
            if selection=='q':
                break #break station selection loop for given city, state
            if (s:=int(selection)-1) in range(n):
                station_id=stations[s][0].strip() #strip leading and trailing whitespace
                if (os.path.isfile(station_id+'.csv') or os.path.isfile(station_id+'.dly')) and input('Reload? \'y\'/<any other key>: ')!='y':
                    print('Opening file of existing data for station '+station_id+' ...')
                    try:
                        df=pd.read_csv(station_id+'.csv', low_memory=False)
                    except FileNotFoundError: #have the .dly file, read it into df and also create .csv
                        df=w.dly_to_csv(station_id+'.dly',station_id)

                else:
                    print('(Re-)Loading data for station '+station_id+' ...')
                    response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/'+station_id+'.dly')
                    with open(station_id+'.dly', 'w') as file:
                        file.write(response.text)
                    df=w.dly_to_csv(station_id+'.dly',station_id)
                    
                print(f'Retrieved data for {city}, {state} at station {station_id}.')
                w.make_prcp_plot_20(df,f'Precipitation and Wind in {city}, {state}')

    q=input('Quit? \'y\'/<any other key>: ')
    if q=='y':
        break #end program
