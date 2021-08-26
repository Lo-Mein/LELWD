import pickle
import functools
import requests
from requests.models import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import doAlert

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

def parse_data(data):
    days = ["day1", "day2", "day3"]
    graph_data = [[], [], []]
    for i in range(len(days)):
        current = data[days[i]]
        for index in range(len(current)):
            graph_row = current[index]["Mw"]
            graph_data[i].append(graph_row)
    return graph_data


if __name__ == "__main__":
    file_name = "forecast.pkl"
    with open(file_name, "rb") as open_file:
        loaded_forecast = pickle.load(open_file)
    #Load the current forecast
    data = retrieve_data()
    parsed_data = parse_data(data)
    updated_forecast = parsed_data[0]

    #Check whether the forecast has been changed
    if functools.reduce(lambda x, y : x and y, map(lambda p, q: p != q,loaded_forecast,updated_forecast), True): 
        with open(file_name, "wb") as open_file:
            pickle.dump(parsed_data[0], open_file)
        body = """\
        <html>
            <head>
                <meta charset="UTF-8">
                <link rel='stylesheet' type='text/css' media='screen' href='df_style.css'>
            </head>
            <body>
                <p style="font-family: Verdana; font-size: 14px;">	
                    Today's Forecast has changed. Check out the new forecast below. <br>
                    <a href="https://www.iso-ne.com/markets-operations/system-forecast-status/three-day-system-demand-forecast">New Forecast</a>
                </p>
            </body>
        </html>
        """
        doAlert.send_alert(body, "Forecast Update")

    
        