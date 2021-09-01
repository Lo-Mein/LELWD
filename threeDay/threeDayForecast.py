import requests
import pickle
from requests.models import HTTPBasicAuth
import pandas as pd
import numpy as np
import datetime
import doMail
import matplotlib.pyplot as plt
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xmltodict
from mongoConnect import get_monthly_historical_data

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def retrieve_data():
    three_day_api = (
        "https://www.iso-ne.com/ws/wsclient?_ns_requestType=threedayforecast"
    )
    response = requests.get(
        three_day_api,
        auth=HTTPBasicAuth("info.rmsolutionss@gmail.com", "JeffKramer1"),
        verify=False,
    )
    json_data = response.json()
    return json_data[0]["data"]


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


def get_six_day():
    d = datetime.date.today()
    api_date = "{}{:02d}{:02d}".format(d.year, d.month, d.day)
    six_day_api = "https://webservices.iso-ne.com/api/v1.1/sevendayforecast/day/{}".format(
        api_date)
    response = requests.get(
        six_day_api,
        auth=HTTPBasicAuth("info.rmsolutionss@gmail.com", "JeffKramer1"),
        verify=False,
    )
    xml_data = response.content
    xml_dict = xmltodict.parse(xml_data)

    parsed_dict = xml_dict["SevenDayForecasts"]["SevenDayForecast"]["MarketDay"]
    return [int(parsed_dict[i]["PeakLoadMw"]) for i in range(len(parsed_dict))]

# Foramt the data in a way that each hour of each day displays the correct Mw


def parse_data(data):
    days = ["day1", "day2", "day3"]
    graph_data = [[], [], []]
    table_data = [[], [], []]
    for i in range(len(days)):
        current = data[days[i]]
        for index in range(len(current)):
            graph_row = current[index]["Mw"]
            graph_data[i].append(graph_row)
            table_row = "{:,}".format(current[index]["Mw"])
            table_data[i].append(table_row)
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
    plt.legend(title="Days", loc=3)
    plt.axhline(y=threshold_1, color='red')
    plt.axhline(y=threshold_2, color='black')
    plt.xlabel("Hour End")
    plt.ylabel("MWh")
    plt.title("Three Day Forecast")
    plt.savefig("figure.png")
    plt.close()


def create_pie_chart(data):
    # Data going into the chart
    labels = []
    sizes = []
    for x, y in data.items():
        labels.append("Hour End " + str(x))
        sizes.append(y)

    colors = ["gold", "yellowgreen", "lightcoral", "lightskyblue"]
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
    plt.savefig("figure2.png")
    plt.close()


def create_bar_chart(threshold1, threshold2):
    peak_loads = get_six_day()

    day1 = datetime.date.today()
    day2 = day1 + datetime.timedelta(days=1)
    day3 = day1 + datetime.timedelta(days=2)
    day4 = day1 + datetime.timedelta(days=3)
    day5 = day1 + datetime.timedelta(days=4)
    day6 = day1 + datetime.timedelta(days=5)

    days = [
        day1.strftime("%m/%d/%y"),
        day2.strftime("%m/%d/%y"),
        day3.strftime("%m/%d/%y"),
        day4.strftime("%m/%d/%y"),
        day5.strftime("%m/%d/%y"),
        day6.strftime("%m/%d/%y"),
    ]

    plt.bar(days, peak_loads, color='#c4d79b')
    # plt.grid(color='#95a5a6', linestyle='solid', linewidth=1, axis='y')
    plt.title("Six Day Forecast")
    plt.ylabel("MWH")
    plt.axhline(y=threshold1, color='royalblue',
                lw=1.5, label="Historical Threshold")
    plt.axhline(y=threshold2, color='orange', lw=1.5,
                label="Current Month Threshold")
    plt.legend(loc='lower left', mode='expand', ncol=3)
    plt.savefig("figure3.png")
    plt.close()


def get_peak_data(data):

    peak_1, peak_2, peak_3 = max(data[0]), max(data[1]), max(data[2])
    hour_peak_1, hour_peak_2, hour_peak_3 = (
        data[0].index(peak_1) + 1,
        data[1].index(peak_2) + 1,
        data[2].index(peak_3) + 1,
    )

    return peak_1, peak_2, peak_3, hour_peak_1, hour_peak_2, hour_peak_3


def current_month_threshold():
    d = datetime.date.today()
    month_data = []
    for day in range(1, d.day):
        api_date = "{}{:02d}{:02d}".format(d.year, d.month, day)
        api_data = retrieve_actual_data(api_date)
        day_peak = float(0)
        for i in range(len(api_data)):
            day_data = float(api_data[i]["Load"])
            if day_data > day_peak:
                day_peak = day_data
        month_data.append(day_peak)

    if not month_data:
        return 0

    return round(max(month_data) * .97)


def alert_rating(peak, threshold):
    if threshold == 0:
        decision = "N/A"
        rating = "N/A"
        color = '#c4d79b'
        return rating, decision, color

    difference = peak - threshold

    if difference < -1000:
        decision = "No"
        rating = 0
        color = '#c4d79b'
    elif difference <= -500:
        decision = "No"
        rating = 1
        color = '#d8e4bc'
    elif difference <= 0:
        decision = "No"
        rating = 2
        color = '#ebf1de'
    elif difference <= 500:
        decision = "Yes"
        rating = 3
        color = '#f2dcdb'
    elif difference <= 1000:
        decision = "Yes"
        rating = 4
        color = '#e6b8b7'
    else:
        decision = "Yes"
        rating = 5
        color = '#da9694'

    return rating, decision, color


# sourcery skip: ensure-file-closed
if __name__ == "__main__":
    data = retrieve_data()
    table_data, graph_data = parse_data(data)

    file_name = "../alertSystem/forecast.pkl"
    open_file = open(file_name, "wb")
    pickle.dump(graph_data[0], open_file)
    open_file.close()

    table_df = format_data(table_data)
    graph_df = format_data(graph_data)

    peak_1, peak_2, peak_3, hour_peak_1, hour_peak_2, hour_peak_3 = get_peak_data(
        graph_data
    )

    pie_data, threshold = get_monthly_historical_data()
    historical_threshold = np.percentile(threshold, 75)
    monthly_threshold = current_month_threshold()

    if historical_threshold > monthly_threshold:
        alert_threshold = historical_threshold
    else:
        alert_threshold = monthly_threshold

    pie_data.sort()
    pie_dict = {i: pie_data.count(i) for i in pie_data}

    create_bar_chart(historical_threshold, monthly_threshold)
    create_pie_chart(pie_dict)
    create_line_chart(graph_df, historical_threshold, monthly_threshold)

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    third_day = today + datetime.timedelta(days=2)

    today = today.strftime("%m/%d/%y")
    tomorrow = tomorrow.strftime("%m/%d/%y")
    third_day = third_day.strftime("%m/%d/%y")

    rating, decision, color = alert_rating(peak_1, alert_threshold)

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
            <td style="border: 1px solid black; border-collapse: collapse; background: {14}">{10}</td>
         </tr>
         <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Turn on Battery/Generator?</th>
            <td style="border: 1px solid black; border-collapse: collapse;">{11}</td>
         </tr>
    </table>
        <img style="float:left; width: 375px; height: 275px; padding-left: 25px;" src="cid:image2">
        
    <table style="border: 1px solid black; border-collapse: collapse; float: left;">
        <tr>
            <th colspan="3" style="border: 1px solid black; border-collapse: collapse; column-span: all;">
               <h3>Three Day Forecast</h3>
            </th>
        </tr>
        <tr>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Date:</th>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Projected Peak</th>
            <th style="border: 1px solid black; border-collapse: collapse; text-align: left;">Hour End</th>
        </tr>
        <tr>
            <td style="border: 1px solid black; border-collapse: collapse;">{7} (Today)</td>
            <td style="border: 1px solid black; border-collapse: collapse;">{0}</td>
            <td style="border: 1px solid black; border-collapse: collapse;">{1}</td>
         </tr>
         <tr>
            <td style="border: 1px solid black; border-collapse: collapse;">{12}</td>
            <td style="border: 1px solid black; border-collapse: collapse;">{2}</td>
            <td style="border: 1px solid black; border-collapse: collapse;">{3}</td>
         </tr>
         <tr>
            <td style="border: 1px solid black; border-collapse: collapse;">{13}</td>
            <td style="border: 1px solid black; border-collapse: collapse;">{4}</td>
            <td style="border: 1px solid black; border-collapse: collapse;">{5}</td>
         </tr>
    </table>
    
    <div style="clear: both;"></div>

        <div style="font-family: Verdana; font-size: 14px; float: left; margin-top: 40px;">
            {6}
        </div>
        <img style="float:left; width: 630px; height: 462px;" src="cid:image1">
        <div style="clear: both;"></div>

        <img style="float:left; width: 630px; height: 462px;" src="cid:image3">

        <table style="width:100%; height: 500px;">
        <caption style="font-family: Verdana; font-size: 14px; text-align: left;">	
        <b>Historical Threshold:</b>
        Is equal to the 75th percentile of historical peak loads of the current month over the last five years.</caption>
        <caption style="font-family: Verdana; font-size: 14px; text-align: left;">
        <b>Current Month Threshold:</b>
        Is equal to 97% of the Month's Peak to date.
        </caption>
        <tr>
            <th COLSPAN="6" style="height: 50px; border: 1px solid black; border-collapse: collapse; width:100%;">
               <h3 style=" font: bold 20px Georgia, serif;height: 80px; "><br>Alert Ratings Explained</h3>
            </th>
        </tr>
 
            <tr border: 1px solid black;>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background: #c4d79b; border: 1px solid black; font: 14px Arial, sans-serif;">0</td>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background: #d8e4bc; border: 1px solid black; font: 14px Arial, sans-serif;">1</td>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background: #ebf1de; border: 1px solid black; font: 14px Arial, sans-serif;">2</td>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background:#f2dcdb; border: 1px solid black; font: 14px Arial, sans-serif;">3</td>                        
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background:#e6b8b7; border: 1px solid black; font: 14px Arial, sans-serif;">4</td>
                <td scope="col" style="padding:0in 5.4pt 0in 5.4pt; background:#da9694; border: 1px solid black; font: 14px Arial, sans-serif;">5</td>
            </tr>
            <tr >
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #c4d79b; border: 1px solid black; font: 14px Arial, sans-serif;">Projected peak is below the threshold by greater than 1,000 MW. </td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #d8e4bc; border: 1px solid black; font: 14px Arial, sans-serif;">Projected peak is below the threshold by an amount between 500 and 1,000 MW.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #ebf1de; border: 1px solid black; font: 14px Arial, sans-serif;">Projected peak is below the threshold by an amount less than 500 MW.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#f2dcdb; border: 1px solid black; font: 14px Arial, sans-serif;">Projected peak is above the threshold by an amount less than 500 MW.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#e6b8b7; border: 1px solid black; font: 14px Arial, sans-serif;">Projected peak is above the threshold by an amount between 500 and 1,000 MW.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#da9694; border: 1px solid black; font: 14px Arial, sans-serif;">Projected peak is above the threshold by an amount greater than 1,000 MW.</td>
            </tr>
            <tr >
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #c4d79b; border: 1px solid black; font: 14px Arial, sans-serif;">Take no action.  This will not be the peak day. </td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #d8e4bc; border: 1px solid black; font: 14px Arial, sans-serif;">Take no action.  Barring a dramatic miss by ISO this will not be the peak day.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background: #ebf1de; border: 1px solid black; font: 14px Arial, sans-serif;">Be aware of the situation.  Peak load is approaching threshold, but will most likely not be the peak.</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#f2dcdb;border: 1px solid black; font: 14px Arial, sans-serif;">Send alert.  Today has a chance of being the peak day</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#e6b8b7;border: 1px solid black; font: 14px Arial, sans-serif;">Send alert.  There is a strong chance that today will be the peak day</td>
                <td style="padding:0in 5.4pt 0in 5.4pt; background:#da9694;border: 1px solid black; font: 14px Arial, sans-serif;">Send alert.  There is an extremely  high probability that today will be the peak day. </td>
            </tr>
    </table>


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
        decision,
        tomorrow,
        third_day,
        color

    )
    doMail.send_mail(body)
