import requests
import json
from requests.models import HTTPBasicAuth
import pandas as pd 
import numpy as np
import datetime
from IPython.display import HTML
import doMail



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
            'Hour 01', 'Hour 02', 'Hour 03', 'Hour 04', 'Hour 05', 'Hour 06', 
            'Hour 07', 'Hour 08', 'Hour 09', 'Hour 10', 'Hour 11', 'Hour 12', 
            'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18', 
            'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
            ],
        index= days
    )
    df = df.transpose()
    return df
    





if __name__ == "__main__":
    data = retrieveData()
    data = parseData(data)
    df = formatData(data)
    body = df.to_html()
    doMail.send_mail(body)
