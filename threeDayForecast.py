import requests
import json
from requests.models import HTTPBasicAuth
import pandas as pd
import numpy as np
import datetime
from IPython.display import HTML
import doMail
import matplotlib.pyplot as plt
import csv

# import schedule
import time


# Get the desired data from the api
def retrieve_data():
    seven_day_api = (
        "https://www.iso-ne.com/ws/wsclient?_ns_requestType=threedayforecast"
    )
    response = requests.get(
        seven_day_api, auth=HTTPBasicAuth("info.rmsolutionss@gmail.com", "JeffKramer1")
    )
    json_data = response.json()
    demand_data = json_data[0]["data"]

    return demand_data


# Foramt the data in a way that each hour of each day displays the correct Mw
def parse_data(data):
    days = ["day1", "day2", "day3"]
    mw_data = [[], [], []]
    i = 0
    while i < len(days):
        current = data[days[i]]
        for index in range(len(current)):
            row = current[index]["Mw"]
            mw_data[i].append(row)
        i += 1
    get_peak_data(mw_data)
    return mw_data


def format_data(data):
    day1 = datetime.date.today()
    day2 = day1 + datetime.timedelta(days=1)
    day3 = day1 + datetime.timedelta(days=2)

    days = [
        day1.strftime("%m/%d/%y"),
        day2.strftime("%m/%d/%y"),
        day3.strftime("%m/%d/%y"),
    ]

    df = pd.DataFrame(
        data,
        columns=[
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24
            # 'Hour 01', 'Hour 02', 'Hour 03', 'Hour 04', 'Hour 05', 'Hour 06',
            # 'Hour 07', 'Hour 08', 'Hour 09', 'Hour 10', 'Hour 11', 'Hour 12',
            # 'Hour 13', 'Hour 14', 'Hour 15', 'Hour 16', 'Hour 17', 'Hour 18',
            # 'Hour 19', 'Hour 20', 'Hour 21', 'Hour 22', 'Hour 23', 'Hour 24'
        ],
        index=[days],
    )
    df = df.transpose()
    df.style

    return df


def create_line_chart(df):
    df.plot.line()
    plt.xticks(
        [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
        ]
    )
    plt.xlabel("Hour End")
    plt.ylabel("MWh")
    plt.title("Three Day Forecast")
    plt.savefig("figure.png")


def get_peak_data(data):

    peak_1, peak_2, peak_3 = max(data[0]), max(data[1]), max(data[2])
    hour_peak_1, hour_peak_2, hour_peak_3 = (
        data[0].index(peak_1) + 1,
        data[1].index(peak_2) + 1,
        data[2].index(peak_3) + 1,
    )

    return peak_1, peak_2, peak_3, hour_peak_1, hour_peak_2, hour_peak_3


# rework function
def save_as_csv(data):

    item_count = 0

    with open("test.csv", "w", newline="") as csvfile:
        column_names = ["HourEnd", "Mw"]

        the_writer = csv.DictWriter(csvfile, fieldnames=column_names)

        the_writer.writeheader()

        for item in data:
            item_count += 1
            the_writer.writerow({"HourEnd": item_count, "Mw": item})


if __name__ == "__main__":
    data = retrieve_data()
    data = parse_data(data)
    # data = save_as_csv(data)
    df = format_data(data)
    peak_1, peak_2, peak_3, hour_peak_1, hour_peak_2, hour_peak_3 = get_peak_data(data)
    create_line_chart(df)
    body = """\
    <html>
    <head></head>
    <body>
        <p style="font-family: Verdana; font-size: 20px;">
            This is a hourly systemwide demand forecast for today and the next two days. This is the expected amount of electricity to be used in the New England Balancing Authority Area (BAA): Connecticut, Rhode Island, Massachusetts, Vermont, New Hampshire, and most of Maine. The forecast is updated twice daily at 6:00 a.m. and 10:00 a.m. eastern prevailing time.<br><br>
            <strong>Today's Projected Peak (MW)</strong> {0} at HE {1}<br>
            <strong>Tomorrow's Projected Peak (MW)</strong> {2} at HE {3}<br>
            <strong>Day Three Projected Peak (MW)</strong> {4} at HE {5}<br>
        </p>
        <div style="font-family: Verdana; font-size: 20px; float: left; margin-top: 40px;">
            {6}
        </div>
        <img style="float:right; width: 750px; height: 550px;" src="cid:image1">
      
      
    </body>
    </html>
    """.format(
        peak_1, hour_peak_1, peak_2, hour_peak_2, peak_3, hour_peak_3, df.to_html()
    )

    # schedule.every().day.at("15:00").do(doMail.send_mail, body)
    doMail.send_mail(body)

# while True:
#     schedule.run_pending()
#     time.sleep(2)
