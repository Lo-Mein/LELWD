from numpy.lib.function_base import diff
import requests
from requests.models import HTTPBasicAuth
import pandas as pd
import numpy as np
import datetime
import doMail
import matplotlib.pyplot as plt
import csv
from itertools import chain
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xmltodict


from mongoConnect import get_monthly_historical_data


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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


def retrieve_actual_data(api_date):
    actual_data_api = "https://webservices.iso-ne.com/api/v1.1/hourlysysload/day/{}/location/32".format(
        api_date
    )
    response = requests.get(
        actual_data_api,
        auth=HTTPBasicAuth("info.rmsolutionss@gmail.com", "JeffKramer1"),
        verify=False,
    )
    xml_data = response.content
    xml_dict = xmltodict.parse(xml_data)

    return xml_dict["HourlySystemLoads"]["HourlySystemLoad"]


def current_month_threshold():
    d = datetime.date.today()
    month_data = []
    for day in range(1, d.day):
        api_date = "{}{:02d}{:02d}".format(d.year, d.month, day)
        api_data = retrieve_actual_data(api_date)
        day_peak = float(0)
        for i in range(23):
            day_data = float(api_data[i]["Load"])
            if day_data > day_peak:
                day_peak = day_data
        month_data.append(day_peak)
    
    if len(month_data) == 0:
        return 0
    
    return round(max(month_data) * .97)

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


def create_line_chart(df, threshold_1, threshold_2):
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
    plt.legend(title= "Days", loc= 3)
    plt.axhline(y=threshold_1, color='red')
    plt.axhline(y=threshold_2, color='black')
    plt.xlabel("Hour End")
    plt.ylabel("MWh")
    plt.title("Three Day Forecast")
    plt.savefig("./threeDay/figure.png")


def create_pie_chart(data):
    # Data going into the chart
    labels = []
    sizes = []
    for x, y in data.items():
        labels.append("Hour End " + str(x))
        sizes.append(y)

    # hours_end = data[0]
    # length = len(hours_end)
    # middle_index = length // 3
    # last_half = hours_end[:middle_index]
    # pie_list = []
    # for i in last_half:
    #     i = float(i.replace(",", ""))
    #     pie_list.append([i])
    #     i += 1
    # pie_list2 = list(chain.from_iterable(pie_list))

    colors = ["gold", "yellowgreen", "lightcoral", "lightskyblue"]
    explode = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    # Plot the data
    plt.pie(
        sizes,
        # explode=explode,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        shadow=True,
        startangle=140,
    )
    month = datetime.datetime.now()
    month = month.strftime("%B")
    plt.title(month + "'s Year Historical Peak Hour")
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


def alert_rating(peak, threshold):
    if threshold == 0:
        decision = "N/A"
        rating = "N/A"
        return rating, decision

    difference = peak - threshold

    if difference < -1000:
        decision = "No"
        rating = 0
    elif difference >= -1000 and difference <= -500:
        decision = "No"
        rating = 1
    elif difference > -500 and difference <= 0:
        decision = "No"
        rating = 2
    elif difference > 0 and difference <= 500:
        decision = "Yes"
        rating = 3
    elif difference > 500 and difference <= 1000:
        decision = "Yes"
        rating = 4
    elif difference > 1000:
        decision = "Yes"
        rating = 5

    return rating, decision

if __name__ == "__main__":
    data = retrieve_data()
    table_data, graph_data = parse_data(data)

    table_df = format_data(table_data)
    graph_df = format_data(graph_data)

    peak_1, peak_2, peak_3, hour_peak_1, hour_peak_2, hour_peak_3 = get_peak_data(
        graph_data
    )

    pie_data, threshold = get_monthly_historical_data()
    historical_threshold = np.percentile(threshold, 75)
    monthly_threshold = current_month_threshold()

    pie_data.sort()
    pie_dict = {i: pie_data.count(i) for i in pie_data}

    create_pie_chart(pie_dict)
    create_line_chart(graph_df, historical_threshold, monthly_threshold)

    today = datetime.date.today()
    today = today.strftime("%m/%d/%y")

    rating, decision = alert_rating(peak_1, monthly_threshold)
    body = """\
    <html>
   
    <head>
        <meta charset="UTF-8">
        <link rel='stylesheet' type='text/css' media='screen' href='df_style.css'>
    </head>
    <style type="text/css">
  
    </style>
    <body>
    <table style="border: 1px solid black; border-collapse: collapse; float: left;">
        <tr>
            <th colspan="6" style="border: 1px solid black; border-collapse: collapse; column-span: all;">
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
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Historical Threshold:</th>
            <td style="border: 1px solid black; border-collapse: collapse;">{8}</td>
         </tr>
         <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Current Month Threshold:</th>
            <td style="border: 1px solid black; border-collapse: collapse;">{9}</td>
         </tr>
         <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Alert Rating:</th>
            <td style="border: 1px solid black; border-collapse: collapse;">{10}</td>
         </tr>
         <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Turn on Battery/Generator?</th>
            <td style="border: 1px solid black; border-collapse: collapse;">{11}</td>
         </tr>
    </table>
        <img style="float:left; width: 375px; height: 275px; padding-left: 25px;" src="cid:image2">
        <div style="clear: both;"></div>
        <p  style="font-family: Verdana; font-size: 18px; float: left;">
            <strong class="upTop">Today's Projected Peak (MW)</strong> {0} at HE {1}<br>
            <strong>Tomorrow's Projected Peak (MW)</strong> {2} at HE {3}<br>
            <strong>Day Three Projected Peak (MW)</strong> {4} at HE {5}<br>
        </p>
    
    <table style="width:100%; height: 500px;">
        <caption style="font-family: Verdana; font-size: 18px;">	
        <b>Threshold 1:</b>
        Is equal to the 81st percentile of historical peak loads of the current month over the last five years.  This threshold gradually decreases until the end of the month, where it is equal to the 67th percentile.</caption>
        <caption style="font-family: Verdana; font-size: 18px; ">
        <b>Threshold 2:</b>
        Is equal to 97% of the Month's Peak to date.
        </caption>
        <tr>
            <th COLSPAN="6" style="height: 50px; border: 1px solid black; border-collapse: collapse; width:100%;">
               <h3 style=" font: bold 35px Georgia, serif;height: 80px; "><br>Alert Ratings Explained</h3>
            </th>
        </tr>
 
            <tr border: 1px solid black;>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background: #c4d79b; border: 1px solid black; font: 20px Arial, sans-serif;">0</td>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background: #d8e4bc; border: 1px solid black; font: 20px Arial, sans-serif;">1</td>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background: #ebf1de; border: 1px solid black; font: 20px Arial, sans-serif;">2</td>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background:#f2dcdb; border: 1px solid black; font: 20px Arial, sans-serif;">3</td>                        
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background:#e6b8b7; border: 1px solid black; font: 20px Arial, sans-serif;">4</td>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background:#da9694; border: 1px solid black; font: 20px Arial, sans-serif;">5</td>
            </tr>
            <tr >
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #c4d79b; border: 1px solid black; font: 20px Arial, sans-serif;">Projected peak is below the threshold by greater than 1,000 MW. </td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #d8e4bc; border: 1px solid black; font: 20px Arial, sans-serif;">Projected peak is below the threshold by an amount between 500 and 1,000 MW.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #ebf1de; border: 1px solid black; font: 20px Arial, sans-serif;">Projected peak is below the threshold by an amount less than 500 MW.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#f2dcdb; border: 1px solid black; font: 20px Arial, sans-serif;">Projected peak is above the threshold by an amount less than 500 MW.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#e6b8b7; border: 1px solid black; font: 20px Arial, sans-serif;">Projected peak is above the threshold by an amount between 500 and 1,000 MW.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#da9694; border: 1px solid black; font: 20px Arial, sans-serif;">Projected peak is above the threshold by an amount greater than 1,000 MW.</td>
            </tr>
            <tr >
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #c4d79b; border: 1px solid black; font: 20px Arial, sans-serif;">Take no action.  This will not be the peak day. </td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #d8e4bc; border: 1px solid black; font: 20px Arial, sans-serif;">Take no action.  Barring a dramatic miss by ISO this will not be the peak day.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #ebf1de; border: 1px solid black; font: 20px Arial, sans-serif;">Be aware of the situation.  Peak load is approaching threshold, but will most likely not be the peak.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#f2dcdb;border: 1px solid black; font: 20px Arial, sans-serif;">Send alert.  Today has a chance of being the peak day</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#e6b8b7;border: 1px solid black; font: 20px Arial, sans-serif;">Send alert.  There is a strong chance that today will be the peak day</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#da9694;border: 1px solid black; font: 20px Arial, sans-serif;">Send alert.  There is an extremely  high probability that today will be the peak day. </td>
            </tr>
    </table>
        <img style="float:right; width: 750px; height: 550px;" src="cid:image1">
        <div style="font-family: Verdana; font-size: 20px; float: left; margin-top: 40px;">
            {6}
        </div>
     
        <div style="clear: both;"></div>


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
        today,
        historical_threshold,
        monthly_threshold,
        rating,
        decision
        
    )
    doMail.send_mail(body)
