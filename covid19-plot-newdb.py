import matplotlib.pyplot as plt
import array
import matplotlib.dates as dates
import csv
import datetime as datetime
import requests
import json
import matplotlib.ticker as ticker
from urllib.parse import quote

from subprocess import check_output

def firstnonzero(a):
    return [i for i, e in enumerate(a) if e != 0][0]

states=['NY','NJ','PA','FL','CA','SC','TX']
jl = []
for state in states:
    r=requests.get('https://covidtracking.com/api/v1/states/{}/daily.json'.format(quote(state.lower())))
    jtext = r.json()
    timeaxis = []
    data = []
    data0 = []
    for record in jtext:
        try:
            if type(record['deathIncrease']) is int:
                if record['dateChecked'] != 'None':
                    timeaxis.append( dates.datestr2num(record['dateChecked'] ) )
                    data0.append( int(record['deathIncrease']))                
        except :
            pass
    for i in range(0, len(data0) -8):
        data.append(sum(data0[i:i+7]) / 7)
        #if state != 'NY':
        #    data.append(sum(data0[i:i+7]) / 7)
        #else:
        #    data.append(sum(data0[i:i+4]) / 4)
#            data.append(data0[i])
    plt.plot(timeaxis[0:len(timeaxis)-8], data)
#    plt.plot(timeaxis, data0)

plt.gca().set_xlim(left = dates.datestr2num('2020-05-19T00:00:00Z'))
plt.gca().set_ylim(bottom = 0, top = 400)
plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(dates.DayLocator(interval=7))
plt.gca().xaxis.set_minor_locator(dates.DayLocator(interval=1))
plt.legend(states)
plt.ylabel('COVID-19')
plt.grid(axis='y')
#plt.yscale("log")
#plt.show()
figfilename = 'COVID19_TriState.png'
plt.savefig(figfilename)
check_output(figfilename, shell=True)