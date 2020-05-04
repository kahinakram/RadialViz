from flask import Flask, render_template, url_for, request,jsonify
import numpy as np 
import pandas as pd 
import json
import operator
import time
import random
import glob
#Initialize Flask App
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rawdata')
def organizeDataToJson(date_time,value_array=None):

    dictionary = dict()
    i = 0
    for stamp in date_time:
        #Create the key being the day
        datestr = '{}-{}-{}'.format(stamp.year, stamp.month, stamp.day)

        if datestr not in dictionary:
             dictionary[datestr] = { 'AM' : [ 0 for x in range(12) ], 'PM' : [ 0 for x in range(12) ] }
        
        if value_array is None:
            if stamp.hour < 12:
                    dictionary[datestr]['AM'][stamp.hour] += 1
            else:
                dictionary[datestr]['PM'][stamp.hour - 12] += 1
        else:
            if stamp.hour < 12:
                dictionary[datestr]['AM'][stamp.hour] += value_array[i]
            else:
                dictionary[datestr]['PM'][stamp.hour - 12] += value_array[i]
        i+=1
    
    return json.dumps(dictionary)

@app.route('/musicdata')
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

    return json.dumps(dd)

@app.route('/createcsv', methods=['POST'])
def createcsv():

    # POST request
    if request.method == 'POST':
        print('Saving Client data as CSV')
        
        #since all the arrays are not the same length
        jsonObj = request.get_json(force=True)
        fileName = jsonObj['fileName']
        answers = jsonObj['answers']
        df = pd.DataFrame.from_dict(answers)
        
        #path = '/Users/home/Documents/Work/Projects/6 - Radial Visualization/test_images/Answers/'
        path = '/Users/home/Documents/Work/Projects/6 - Radial Visualization/images/Exp2/Correct-Answers-Experiment-2/'
        df.to_csv(path+fileName+'.csv',sep=',')
        
        #df.to_csv("data.csv")
        return 'Data saved as csv file!', 200
    
'''Experiment 1'''

@app.route('/stackedbarchart')
def stackedbarchart():
    return render_template('stackedbarchart.html', 
    humidityData=humidityData, 
    trafficData=trafficData, 
    energyData=energyData, 
    uberData=uberData) 

@app.route('/adjacentbarchart')
def adjacentbarchart():
    return render_template('adjacentbarchart.html', 
    humidityData=humidityData, 
    trafficData=trafficData, 
    energyData=energyData, 
    uberData=uberData)   

@app.route('/combinedbarchart')
def combinedbarchart():
    return render_template('combinedbarchart.html', 
    humidityData=humidityData, 
    trafficData=trafficData, 
    energyData=energyData, 
    uberData=uberData)   

'''Experiment 2'''

@app.route('/overlaidbarchart')
def overlaidbarchart():
    return render_template('overlaidbarchart.html', 
    humidityData=humidityData, 
    trafficData=trafficData, 
    energyData=energyData, 
    uberData=uberData) 

@app.route('/layeredbarchart')
def layeredbarchart():
    return render_template('layeredbarchart.html', 
    humidityData=humidityData, 
    trafficData=trafficData, 
    energyData=energyData, 
    uberData=uberData) 

@app.route('/rosebarchart')
def rosebarchart():
    return render_template('rosebarchart.html', 
    humidityData=humidityData, 
    trafficData=trafficData, 
    energyData=energyData, 
    uberData=uberData) 

''' End '''

def createHumidityJson(data):
    dictionary = dict()
    data['date_time'] = pd.to_datetime(data['date_time'])
    data['Phoenix'] = data['Phoenix'].round(0) #time consuming 
    
    i = 0
    for stamp in data['date_time']:
        #Create the key being the day
        datestr = '{}-{}-{}'.format(stamp.year, stamp.month, stamp.day)

        if datestr not in dictionary:
            dictionary[datestr] = { 
                 'AM' : [ 0 for x in range(12) ], 
                 'PM' : [ 0 for x in range(12) ] 
            }
        if stamp.hour < 12:
            dictionary[datestr]['AM'][stamp.hour] += data['Phoenix'][i]
        else:
            dictionary[datestr]['PM'][stamp.hour - 12] += data['Phoenix'][i]
        i+=1
    
    #return json.dumps(dictionary)
    df = pd.DataFrame.from_dict(dictionary)
    path = '/Users/home/Documents/Work/Projects/6 - Radial Visualization/Experiment/static/data/cleanedJsonData/'
    return df.to_json(path+'PhoenixHumidity.json')
        
def createUberPickupsJson(data):
    dictionary = dict()
    #time consuming 
    data.date_time = pd.to_datetime(data.date_time)

    for stamp in data.date_time:
        #Create the key being the day
        datestr = '{}-{}-{}'.format(stamp.year, stamp.month, stamp.day)

        if datestr not in dictionary:
            dictionary[datestr] = { 
                 'AM' : [ 0 for x in range(12) ], 
                 'PM' : [ 0 for x in range(12) ] 
            }
        if stamp.hour < 12:
            dictionary[datestr]['AM'][stamp.hour] += 1
        else:
            dictionary[datestr]['PM'][stamp.hour - 12] += 1

    return json.dumps(dictionary)
    #df = pd.DataFrame.from_dict(dictionary)
    #path = '/Users/home/Documents/Work/Projects/6 - Radial Visualization/Code/static/data/cleanedCsvData/'
    #return df.to_json(path+'NYCUberPickups.json')

def createNYCTrafficFlowJson(data):
    
    dictionary = dict()
    for stamp in data['date']:
        if stamp not in dictionary:
            dictionary[stamp] = { 
                'AM' : [ 0 for x in range(12) ], 
                'PM' : [ 0 for x in range(12) ] 
            }
    
    for index, row in data.iterrows():
        dictionary[row['date']]['AM'] = [
            row.am0,row.am1,row.am2,
            row.am3,row.am4,row.am5,
            row.am6,row.am7,row.am8,
            row.am9,row.am10,row.am11]
        dictionary[row['date']]['PM'] = [
            row.pm0,row.pm1,row.pm2,
            row.pm3,row.pm4,row.pm5,
            row.pm6,row.pm7,row.pm8,
            row.pm9,row.pm10,row.pm11] 

    return json.dumps(dictionary)
    #df = pd.DataFrame.from_dict(dictionary)
    #path = '/Users/home/Documents/Work/Projects/6 - Radial Visualization/Code/static/data/cleanedCsvData/'
    #return df.to_json(path+'NYCTrafficFlow.json')

def createAmericanEnergyJson(data):
    dictionary = dict()
    data['date_time'] = pd.to_datetime(data['date_time'])

    i = 0
    for stamp in data['date_time']:
        #Create the key being the day
        datestr = '{}-{}-{}'.format(stamp.year, stamp.month, stamp.day)

        if datestr not in dictionary:
            dictionary[datestr] = { 
                 'AM' : [ 0 for x in range(12) ], 
                 'PM' : [ 0 for x in range(12) ] 
            }
        if stamp.hour < 12:
            dictionary[datestr]['AM'][stamp.hour] += data['AEP_MW'][i]
        else:
            dictionary[datestr]['PM'][stamp.hour - 12] += data['AEP_MW'][i]
        i+=1

    #return json.dumps(dictionary)
    df = pd.DataFrame.from_dict(dictionary)
    path = '/Users/home/Documents/Work/Projects/6 - Radial Visualization/Experiment/static/data/cleanedJsonData/'
    return df.to_json(path+'AmericanEnergy.json')

'''These functions have been implemented and do work, 
but need some cleaning... not before the deadline though :) '''
def readEnergyData():
    pass   
    '''
    #~~~~~~~~~~~~~~

    #Sort the data first
    #energy_data_sorted = energy_data.sort_values(
    #    by='Datetime',ascending=True)
    #Energy date time object
    #energy = pd.to_datetime(energy_data_sorted.Datetime)
    energyData = organizeDataToJson(energy_data)
    '''
     
    #Energy Consumption
    #energy_data = pd.read_csv(
    #    'static/data/energy/AmericanEnergy.csv', 
    #    delimiter=',', encoding='utf-8'
    #)

    #createAmericanEnergyJson(energy_data) 

def readWeatherData():
    pass
    #Read weather data
    #relevant_cols_humidity = ['datetime','Phoenix']
    
    #Sort the data first
    #humidity_data_sorted = humidity_data.sort_values(
    #    by='datetime',ascending=True
    #)
    #Replace nan with column average
    #humidity_data_sorted = humidity_data_sorted.groupby(
    #    humidity_data_sorted.columns, axis = 1).transform(
    #        lambda x: x.fillna(random.random()*5))
    #Round the values 
    #humidity_data_sorted = humidity_data_sorted.round(1)
    #Weather date time object
    #humidity = pd.to_datetime(humidity_data_sorted.datetime)


    #~~~~~~~~~~~~~~
    #humidity_data = pd.read_csv(
    #    'static/data/weather/PhoenixHumidity.csv', 
    #    delimiter=',', encoding='utf-8'
    #)

    #createHumidityJson(humidity_data)

def readTrafficFlowData():
    pass
    '''
    Use this in read_csv usecols=relevant_cols_humidity 
    traffic_flow_relevant_cols = [ 
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
    '''
    #traffic_flow_nyc = pd.read_csv(
    #    'static/data/traffic_flow/NYCTrafficFlow.csv', 
    #    delimiter=',', encoding='utf-8'
    #)
    
    #trafficData = createNYCTrafficFlowJson(traffic_flow_nyc)

def readUberPickUpData():
    pass
    '''
    #~~~~~~~~~~~~~~
    #Uber Pick Ups
    #relevant_cols_uber = ['Pickup_date']
    uber_data = pd.read_csv(
        'static/data/uber/NYCUberPickups.csv', 
        delimiter=',', encoding='utf-8',
    #    usecols = relevant_cols_uber
    )

    #uber_data_sorted = uber_data.sort_values(
    #    by='Pickup_date',ascending=True,   
    #)
    #uber_date_time = pd.to_datetime(
    #    uber_data_sorted['Pickup_date']
    #)
    
    '''
    #uber_data = pd.read_csv(
    #    'static/data/uber/NYCUberPickups.csv', 
    #    delimiter=',', encoding='utf-8'
    #)
    #createUberPickupsJson(uber_data)

def notAFunction(just_useful_links):
    pass
    #Parse ISOformat date to datetime
    #youtube_uploads = youtube_uploads.convert_objects(convert_dates='coerce')
    #Check memory usage
    #youtube_uploads.info(memory_usage='deep')
    #https://www.kaggle.com/hanriver0618/2011-2013-nyc-traffic-volume-counts
    #SVG to png image
    #Ciruclar

    #http://bl.ocks.org/kgryte/5926740
    #https://www.d3-graph-gallery.com/graph/circular_barplot_double.html
    #https://www.d3-graph-gallery.com/graph/circular_barplot_label.html
    #https://www.d3-graph-gallery.com/circular_barplot.html
    #https://observablehq.com/@d3/radial-area-chart
    #https://stackoverflow.com/questions/43314115/d3-circular-heat-chart-increase-segment-height-on-mouseover
    #http://bl.ocks.org/jamesleesaunders/0cbfa9ab9bdce220113f
    #https://trengrj.net/2014/06/24/circular-heat-chart.html
    #https://www.peterrcook.com/articles/circularheatchart
    #https://bl.ocks.org/bricedev/8aaef92e64007f882267
    #https://blockbuilder.org/bricedev/0a9bf537a64a55ab1fe8
    #https://embed.plnkr.co/vIwzn3piaBSqTfmVxrKt/

    #Bar
    #http://vis.stanford.edu/jheer/d3/pyramid/shift.html
    #https://bl.ocks.org/d3noob/8952219
    #https://observablehq.com/@d3/stacked-bar-chart
    #https://bl.ocks.org/mbostock/1134768
    #https://www.d3-graph-gallery.com/barplot.html
    #http://bl.ocks.org/yuuniverse4444/8b0e53f29e24e2bdb265
    #https://www.d3-graph-gallery.com/index.html

    #http://jsfiddle.net/g0r9n090/

if __name__ == '__main__':
    
    start = time.time()

    path = '/Users/home/Documents/Work/Projects/6 - Radial Visualization/Experiment/static/data/cleanedJsonData/'

    #read pre-created json files with help from the read(name) function..They do take time.. 
    with open(path+'AmericanEnergy.json') as f: 
        #When json file read it becomes a dict in python
        #We use json.dumps to convert it to json obj
        energyData = json.dumps(json.load(f))

    with open(path+'PhoenixHumidity.json') as f: 
        #When json file read it becomes a dict in python
        #We use json.dumps to convert it to json obj
        humidityData = json.dumps(json.load(f))
    
    with open(path+'NYCTrafficFlow.json') as f: 
        #When json file read it becomes a dict in python
        #We use json.dumps to convert it to json obj
        trafficData = json.dumps(json.load(f))

    with open(path+'NYCUberPickups.json') as f: 
        #When json file read it becomes a dict in python
        #We use json.dumps to convert it to json obj
        uberData = json.dumps(json.load(f))
    
    print(('Execution time for reading the jsons: ', time.time() - start))
    
    app.run(debug=True)
