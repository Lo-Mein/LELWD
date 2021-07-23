import requests
from pandas import DataFrame
import json
from requests.models import HTTPBasicAuth
import pandas as pd
import numpy as np
import datetime
from IPython.display import HTML
import doMail
import matplotlib.pyplot as plt
import csv
from itertools import chain
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# import schedule
import time


# Get the desired data from the api
def retrieve_data():
    seven_day_api = (
        "https://www.iso-ne.com/ws/wsclient?_ns_requestType=threedayforecast"
    )
    response = requests.get(
        seven_day_api,
        auth=HTTPBasicAuth("info.rmsolutionss@gmail.com", "JeffKramer1"),
        verify=False,
    )
    json_data = response.json()
    demand_data = json_data[0]["data"]

    return demand_data


# Foramt the data in a way that each hour of each day displays the correct Mw
def parse_data(data):
    days = ["day1", "day2", "day3"]
    graph_data = [[], [], []]
    table_data = [[], [], []]
    i = 0
    while i < len(days):
        current = data[days[i]]
        for index in range(len(current)):
            graph_row = current[index]["Mw"]
            graph_data[i].append(graph_row)
            table_row = "{:,}".format(current[index]["Mw"])
            table_data[i].append(table_row)
        i += 1
    
    return table_data, graph_data


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
    plt.savefig("./threeDay/figure.png")


def create_pie_chart(data):
    # Data going into the chart
    labels = [
        "End Hour 17",
        "End Hour 18",
        "End Hour 19",
        "End Hour 20",
        "End Hour 21",
        "End Hour 22",
        "End Hour 23",
        "End Hour 24",
    ]
    labeling = list(labels)
    hours_end = data[0]
    length = len(hours_end)
    middle_index = length // 3
    last_half = hours_end[:middle_index]
    pie_list = []
    for i in last_half:
        i = float(i.replace(",", ""))
        pie_list.append([i])
        i += 1
    pie_list2 = list(chain.from_iterable(pie_list))

    colors = ["gold", "yellowgreen", "lightcoral", "lightskyblue"]
    explode = (
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    # Plot the data
    plt.pie(
        pie_list2,
        explode=explode,
        labels=labeling,
        colors=colors,
        autopct="%1.1f%%",
        shadow=True,
        startangle=140,
    )
    day1 = datetime.date.today()
    day1 = str(day1)
    plt.title(day1 + " " + "Mwh values")
    plt.axis("equal")
    # plt.show()
    plt.savefig("./threeDay/figure2.png")


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
            the_writer.writerow({"Day": item_count, "Mw": item})


if __name__ == "__main__":
    data = retrieve_data()
    table_data, graph_data = parse_data(data)
    # data = save_as_csv(data)
    table_df = format_data(table_data)
    graph_df = format_data(graph_data)
    peak_1, peak_2, peak_3, hour_peak_1, hour_peak_2, hour_peak_3 = get_peak_data(table_data) 
    create_pie_chart(table_data)
    create_line_chart(graph_df)
    today = datetime.date.today()
    today = today.strftime("%m/%d/%y")
    body = """\
    <html>
    <head>
        <link rel='stylesheet' type='text/css' media='screen' href='df_style.css'>
    </head>
    <body>
    <table style="border: 1px solid black; border-collapse: collapse;">
        <tr>
            <th COLSPAN="2" style="border: 1px solid black; border-collapse: collapse;">
               <h3><br>Monthly Peak Alert Notice</h3>
            </th>
        </tr>
        <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Date:</th>
            <td style="border: 1px solid black; border-collapse: collapse;">{7}</td>
        </tr>
        <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">ISO Projected Peak:</th>
            <td style="border: 1px solid black; border-collapse: collapse;">{0}</td>
         </tr>
         <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">ISO Projected Hour:</th>
            <td style="border: 1px solid black; border-collapse: collapse;">{1}</td>
         </tr>
         <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Threshold:</th>
            <td style="border: 1px solid black; border-collapse: collapse;">21,883</td>
         </tr>
         <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Alert Rating:</th>
            <td style="border: 1px solid black; border-collapse: collapse;">0</td>
         </tr>
         <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Turn on Battery/Generator?</th>
            <td style="border: 1px solid black; border-collapse: collapse;">No</td>
         </tr>
         <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Hours Ending to Run:</th>
            <td style="border: 1px solid black; border-collapse: collapse;">N/A</td>
         </tr>
    </table>
        <p  style="font-family: Verdana; font-size: 20px;">
            <strong class="upTop">Today's Projected Peak (MW)</strong> {0} at HE {1}<br>
            <strong>Tomorrow's Projected Peak (MW)</strong> {2} at HE {3}<br>
            <strong>Day Three Projected Peak (MW)</strong> {4} at HE {5}<br>
        </p>
        <img style="float:right; width: 750px; height: 550px;" src="cid:image1">
        <img style="float:right; width: 750px; height: 550px;" src="cid:image2">
        <div style="font-family: Verdana; font-size: 20px; float: left; margin-top: 40px;">
            {6}
        </div>

    </body>
    </html>
    """.format(
        peak_1,
        hour_peak_1,
        peak_2,
        hour_peak_2,
        peak_3,
        hour_peak_3,
        table_df.to_html(),
        today
    )
    doMail.send_mail(body)
