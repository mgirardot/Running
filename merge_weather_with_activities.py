# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 08:30:56 2015

@author: Michael
"""

import pandas as pd
f=open("C:/Users/mgirardot/Desktop/garmin_data/OpenWeatherMap_API_key.txt", 'r')
Apikey=f.read()

# importing activities.csv
data = pd.read_csv("C:\Users\mgirardot\Desktop\garmin_data\Activities_format_date.csv", sep='\t')
data


import datetime as dt
d = dt.datetime.strptime(data['date2_heure'][4],'%d/%m/%Y %H:%M')
d

# using open weather map
import pyowm
owm = pyowm.OWM(Apikey)

owm = pyowm.OWM('2344ee7d79650e9caa4464fdbfe0379b')

observation = owm.weather_history_at_place("Montpellier,fr",d, d + dt.timedelta(hours=1))
if not observation :
    print "not ok"
else : print "ok"

w = observation[0]
w.get_status()
temps = w.get_temperature()
temps['temp'] - 273.15

w.get_temperature()['temp']
w.get_humidity()

w.get_wind()['deg']

w.get_rain()['3h']

w.get_clouds()

w.get_pressure()['press']

w.to_JSON()

###############################################################################
data.shape[0]

weather_data = pd.DataFrame(columns=['temp','humidity','wind_speed', 'wind_degree','clouds_coverage', 'rain', 'pressure'])


for i,time_of_run in enumerate(data['date2_heure']):
    d = dt.datetime.strptime(time_of_run,'%d/%m/%Y %H:%M')
    observation = owm.weather_history_at_place("Montpellier,fr",d, d + dt.timedelta(hours=1))
    
    if not observation:
        weather_data.loc[i,:] =('NA', 'NA','NA','NA','NA','NA','NA')
    else:
        w = observation[0]
        weather_data.loc[i,:] =( w.get_temperature()['temp'], w.get_humidity(), w.get_wind()['speed'], 
                                w.get_wind()['deg'], w.get_clouds(), w.get_rain(), w.get_pressure()['press'])
    
weather_data

rain_vol = pd.DataFrame(columns=['rain'])

for i,time_of_run in enumerate(data['date2_heure']):
    d = dt.datetime.strptime(time_of_run,'%d/%m/%Y %H:%M')
    observation = owm.weather_history_at_place("Montpellier,fr",d, d + dt.timedelta(hours=1))

    if not observation:
        rain_vol.loc[i]='NA'
    elif not observation[0].get_rain():
        rain_vol.loc[i]='NA'
    else:
        rain_vol.loc[i]=observation[0].get_rain()['3h']

rain_vol

weather_data['rain']=rain_vol['rain']

df = pd.concat([data, weather_data], axis=1)
df

df.to_csv("C:\Users\Michael\Desktop\garmin_data\Activities_format_date_weather.csv", sep='\t')