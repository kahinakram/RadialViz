import numpy as np 
import pandas as pd 
from collections import Counter
import json
import time 
import operator
from random import randrange

def createMusicDict():

    d = dict()
    dd = dict()
    for stamp in music_data.Date:
        #stamp = datetime.strftime("%Y-%m-%d %H:%M")
        datestr = '{}-{}-{}'.format(stamp.year, stamp.month, stamp.day)
        #print('{}   {}:{}'.format(datestr, stamp.hour, stamp.minute))

        if datestr not in d:
            # create placeholders for am/pm
            d[datestr] = { 'AM' : [ 0 for x in range(12) ], 'PM' : [ 0 for x in range(12) ] }

        if stamp.hour < 12:
            d[datestr]['AM'][stamp.hour] += 1
        else:
            d[datestr]['PM'][stamp.hour - 12] += 1
    
    i = 0
    j = 0 
    for day,value in d.items():
        
        am_array = np.array(value['AM'])
        am_average = np.average(am_array)
        am_array[am_array==0] = int(am_average)

        pm_array = np.array(value['PM'])
        pm_average = np.average(pm_array)
        pm_array[pm_array==0] = int(pm_average)

        if i%6 == 0:
            datestr = 'week_'+str(j)
            if datestr not in dd:
                dd[datestr] = { 'AM' : [ 0 for x in range(12) ], 'PM' : [ 0 for x in range(12) ] }
            j+=1
        
        #print(dd[datestr])
        if am_average > 1:
            dd[datestr]['AM'] = list(map(operator.add, dd[datestr]['AM'], value['AM']))
        if pm_average > 1:
            dd[datestr]['PM'] = list(map(operator.add, dd[datestr]['PM'], value['PM']))

        i+=1

    for week,value in dd.items():
        #
        am_array = np.array(value['AM'])
        am_average = np.average(am_array)
        am_array[am_array==0] = int(am_average) 
        #add the new array
        value['AM'] = am_array.tolist()
        #
        pm_array = np.array(value['PM'])
        pm_average = np.average(pm_array)
        pm_array[pm_array==0] = int(pm_average) 
        #add the new array
        value['PM'] = pm_array.tolist()

    print(json.dumps(dd))
   
def createTemperatureDict():
    date_time = pd.to_datetime(temperature_data.datetime)
    d = dict()
    i = 0
    for stamp in date_time:
        #Create the key being the day
        datestr = '{}-{}-{}'.format(stamp.year, stamp.month, stamp.day)

        if datestr not in d:
             d[datestr] = { 'AM' : [ 0 for x in range(12) ], 'PM' : [ 0 for x in range(12) ] }
        if stamp.hour < 12:
            d[datestr]['AM'][stamp.hour] = temperature_data.Vancouver[i]
        else:
            d[datestr]['PM'][stamp.hour - 12] += temperature_data.Vancouver[i]
        i+=1
    
def createUberPickUpDict():
    d = dict()
    for stamp in uber_date_time:
        #Create the key being the day
        datestr = '{}-{}-{}'.format(stamp.year, stamp.month, stamp.day)

        if datestr not in d:
             d[datestr] = { 'AM' : [ 0 for x in range(12) ], 'PM' : [ 0 for x in range(12) ] }
        if stamp.hour < 12:
            d[datestr]['AM'][stamp.hour] += 1
        else:
            d[datestr]['PM'][stamp.hour - 12] += 1
    
    print(d)

def cleanTrafficData(df):
    df.columns = [
        'Date',
        'am0','am1','am2','am3','am4','am5',
        'am6','am7','am8','am9','am10','am11',
        'pm0','pm1','pm2','pm3','pm4','pm5',
        'pm6','pm7','pm8','pm9','pm10','pm11'
    ]
    
    #df.Date = pd.to_datetime(df.Date)
    
    df_sorted = df.sort_values(by='Date', ascending=True)
    
    d = dict()
    for stamp in df_sorted.Date:

        if stamp not in d:
            d[stamp] = { 
                'AM' : [ 0 for x in range(12) ], 
                'PM' : [ 0 for x in range(12) ] 
            }
    
    for index, row in df_sorted.iterrows():
        d[row.Date]['AM'] = [
            row.am0,row.am1,row.am2,
            row.am3,row.am4,row.am5,
            row.am6,row.am7,row.am8,
            row.am9,row.am10,row.am11]
        d[row.Date]['PM'] = [
            row.pm0,row.pm1,row.pm2,
            row.pm3,row.pm4,row.pm5,
            row.pm6,row.pm7,row.pm8,
            row.pm9,row.pm10,row.pm11]



if __name__ == '__main__':


    relevant_cols = [ 
    'Date','12:00-1:00 AM',
    '1:00-2:00AM','2:00-3:00AM',
    '3:00-4:00AM','4:00-5:00AM',
    '5:00-6:00AM','6:00-7:00AM',
    '7:00-8:00AM','8:00-9:00AM',
    '9:00-10:00AM','10:00-11:00AM',
    '11:00-12:00PM','12:00-1:00PM',
    '1:00-2:00PM','2:00-3:00PM',
    '3:00-4:00PM','4:00-5:00PM',
    '5:00-6:00PM','6:00-7:00PM',
    '7:00-8:00PM','8:00-9:00PM',
    '9:00-10:00PM','10:00-11:00PM',
    '11:00-12:00AM']

    traffic_flow_nyc = pd.read_csv(
        'static/data/traffic_flow/2012-2013.csv', 
        delimiter=',', encoding='utf-8', 
        #optimize, don't read all cols into memory 
        usecols=relevant_cols 
    )
    
    cleanTrafficData(traffic_flow_nyc)
    
    #Read the songs file
    #music_data = pd.read_csv('static/data/music/lonni-music.csv', delimiter=',', encoding='utf-8')
    #music_data.Date = pd.to_datetime(music_data.Date)
    #music_data = music_data.sort_values(by='Date',ascending=True)
    #createMusicDict()


    #temperature_data = pd.read_csv('static/data/temperature-copy.csv', delimiter=',', encoding='utf-8')
    #Replace nan with column average
    #temperature_data = temperature_data.groupby(temperature_data.columns, axis = 1).transform(lambda x: x.fillna(x.mean()))
    #temperature_data = temperature_data.round(1)
    
    #t0 = time.time()
    #uber_data = pd.read_csv(
    #    'static/data/uber-raw-data-janjune-15-copy.csv', 
    #    delimiter=',', encoding='utf-8')
    #uber_date_time = pd.to_datetime(uber_data['Pickup_date'])

    
    #createUberPickUpDict()
    #t1 = time.time()
    #print(t1-t0)
    #createTemperatureDict()
    #createDict(date_time)
