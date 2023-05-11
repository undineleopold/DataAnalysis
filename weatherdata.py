import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import num2date
from matplotlib.widgets import RadioButtons, Slider, RangeSlider, CheckButtons

def get_stations(filename=None,city=None,state=None):
    if not filename or not os.path.isfile(filename): #download file
        response=requests.get('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt') #stations in the network    
        with open('filename', 'w') as file: #write stations to file for future reference
            file.write(response.text)
    #retrieve stations from file
    stations=np.genfromtxt(os.getcwd()+'/'+filename, delimiter=[11,9,10,7,3,31,4,4,6],
                                         names=['id','latitude','longitude','elevation','state','name',
                                                'gsn','hcn','wmo'],
                                         dtype=['U11','d','d','d','U3','U31','U4','U4','U6'],
                                         autostrip=True)
    if city:
        if state:
            stations=stations[np.logical_and(np.char.find(stations['name'],city.upper())==0,stations['state']==state)]
        else:
            stations=stations[np.char.find(stations['name'],city.upper())==0]
    return stations

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

#function returning a restricted df with data from 2020's, missing dates filled
def df_format_20(df):
    #keep only columns which have at least one non-null entry
    df=df[df.columns[df.notnull().sum()>0]]
    cols=list(df.columns.values)
    mask=list(pd.Series(cols).str.match('^(AW|WD|WS|TM|PR)[^B]\w{1}$')) #columns starting AW, WD, WS, TM, or PR, not followed by B,
    #4 characters only (so no flag columns)
    cols=[col for i,col in enumerate(cols) if mask[i]]

    print('Fields available for analysis: ', cols)
    #now restrict the columns to cols+identifying columns, and restrict the date range to the last couple years
    df=df[['STATION','DATE']+cols]
    df=df[df['DATE']>='2020-01-01']

    df.index=pd.DatetimeIndex(df.DATE)
    df=df.reindex(pd.date_range("2020-01-01", pd.to_datetime('today').date()))
    return df

#date plot init
def make_labeled_date_plot(title):
    fig,ax=plt.subplots(figsize=(20,4.5))
    ax.set_title(title)
    plt.setp(ax.get_xticklabels(),rotation=90)
    return fig,ax

#prcp plot update function
def barplot_prcp(df,ax,year,threshr,threshw,direction,complement):
    #check if xlim is correct...the plot is initialized with default values (0.0,1.0) for xlim
    #so this should fail on the first execution and any subsequent time when the year is changed
    if year!=str(num2date(ax.get_xlim()[0]).date().year):
        #set view x-limits for current year
        if pd.to_datetime(year+'-12-31')>df.index[-1]:
            dates=pd.date_range(year+'-01-01',df.index[-1])
        else:
            dates=pd.date_range(year+'-01-01',year+'-12-31')
        ax.set_xlim(xmin=dates[0].date(),xmax=dates[-1].date())
        if len(ax.containers)>0: #already have bars (drawn)
            ax.containers[0].remove() #this works, whereas .pop() does not remove the already drawn artist
                                      #from the canvas, so it comes into view again when xlim is set appropriately
        ax.bar(df.loc[dates].index,df.loc[dates]['PRCP'])#this (re-)creates the barplot artist in ax
        #need the prior call to .remove(), as every call to ax.bar()
        #adds a new barcontainer artist to ax.containers, which is not what we want;
        #to avoid adding and removing the same bar plots repeatedly, would need to make
        #bar plot of all data (2020-2023) and edit the opacity of the correct portion (within current xlim)
    else: #year hasn't changed
        xlims=ax.get_xlim()
        dates=pd.date_range(num2date(xlims[0]).date(),num2date(xlims[1]).date()) 
    mask= (df.loc[dates]['WSF2']>=threshw) & (df.loc[dates]['PRCP']>=threshr)
    if complement:
        mask=mask&((df.loc[dates]['WDF2']<=direction[0]) | (df.loc[dates]['WDF2']>=direction[1]))
    else:
        mask=mask&(df.loc[dates]['WDF2']>=direction[0]) & (df.loc[dates]['WDF2']<=direction[1])
    bars=ax.containers[0]
    for i in range(len(bars)): #update the bars with color and opacity according to mask
        if mask[i]:
            bars[i].set(color='r',alpha=1)
        else:
            bars[i].set(color='k',alpha=0.3)
    ticks=ax.set_xticks(df.loc[dates].loc[mask].index)

#create prcp plot
def make_prcp_plot_20(df,title):
    #check that it has the necessary fields, and dates from 2020-01-01
    df=df_format_20(df)
    
    #initialize plot
    fig,ax=make_labeled_date_plot(title)
    
    #do not plt.show() yet because it is empty and axis labels will be off
    print('Creating plot ...')

    #make room for the controls
    fig.subplots_adjust(left=0.11, bottom=0.5)

    #set y limits and labels
    ax.set_ylim(bottom=0,top=max(df['PRCP']))
    ax.set_ylabel('Precipitation [1/10 mm]')

    #initial values and ranges for controls
    dirmin_init=60
    dirmax_init=140
    rrange=[0,max(df['PRCP'])]
    threshr_init=100
    wrange=[0,400]
    threshw_init=100
    years=['2020','2021','2022','2023']
    year_init=years[-1]

    #create new axes, radio buttons, sliders, and checkbox
    #issues: label sliders with units; allow only integer steps
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
        #checkbutton passed to the actual update function barplot_prcp()
        barplot_prcp(df,ax,y_buttons.value_selected,r_slider.val,w_slider.val,d_slider.val,c_box.get_status()[0]) 
        #one of the following is needed, otherwise the plot does not update correctly
        #fig.canvas.draw()
        fig.canvas.draw_idle() 
    #register sliders and checkbox with the update function
    y_buttons.on_clicked(update)
    r_slider.on_changed(update)
    w_slider.on_changed(update)
    d_slider.on_changed(update)
    c_box.on_clicked(update)
    update(0) #for creating initial plot with default values before controls are changed
    plt.show() #needed to show the actual plot in a window





