import requests
import json
from requests.models import HTTPBasicAuth
import pandas as pd 
import numpy as np
import datetime
from IPython.display import HTML
import doMail
import matplotlib.pyplot as plt



#Get the desired data from the api
def retrieveData():
    sevenDayAPI = "https://www.iso-ne.com/ws/wsclient?_ns_requestType=threedayforecast"
    response = requests.get(sevenDayAPI, auth=HTTPBasicAuth(
        'info.rmsolutionss@gmail.com', 'JeffKramer1'))
    json_data = response.json()
    demandData = json_data[0]['data']

    return demandData


#Foramt the data in a way that each hour of each day displays the correct Mw 
def parseData(data):
    days = ['day1', 'day2', 'day3']
    mwData= [[], [], []]
    i = 0
    while i < len(days):
        current = data[days[i]]
        for index in range(len(current)):
            row = current[index]['Mw']
            mwData[i].append(row)
        i+=1
    getPeakData(mwData)
    return mwData

def formatData(data):
    day1 = datetime.date.today()
    day2 = day1 + datetime.timedelta(days = 1)
    day3 = day1 + datetime.timedelta(days = 2)

    days = [
        day1.strftime("%m/%d/%y"), 
        day2.strftime("%m/%d/%y"), 
        day3.strftime("%m/%d/%y")
        ]


    df = pd.DataFrame(
        data, 
        columns=[ 
            1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24
            # 'Hour 01', 'Hour 02', 'Hour 03', 'Hour 04', 'Hour 05', 'Hour 06', 
            # 'Hour 07', 'Hour 08', 'Hour 09', 'Hour 10', 'Hour 11', 'Hour 12', 
            # 'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
            # 'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
            ],
        index= days
    )
    df = df.transpose()
    
    df.plot.line()
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    plt.xlabel("Hour End")
    plt.ylabel("MWh")
    plt.title("Three Day Forecast")
    plt.show()
    return df

def getPeakData(data):
    peak1, peak2, peak3 = max(data[0]), max(data[1]), max(data[2])

    return peak1, peak2, peak3



if __name__ == "__main__":
    data = retrieveData()
    data = parseData(data)
    df = formatData(data)
    # body = df.to_html()
    # doMail.send_mail(body)
