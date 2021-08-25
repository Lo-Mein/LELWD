import pickle
import functools
import requests
from requests.models import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
    demand_data = json_data[0]["data"]

    return demand_data

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

    return parsed_data


if __name__ == "__main__":
    file_name = "forecast.pkl"
    #Get the forecast from the initial three day forecast charts
    open_file = open(file_name, "rb")
    loaded_forecast = pickle.load(open_file)
    open_file.close()

    #Load the current forecast
    data = retrieve_data()
    parsed_data = parse_data(data)
    updated_forecast = parsed_data[0]
    
    #Check whether the forecast has been changed
    if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,loaded_forecast,updated_forecast), True): 
        print ("The forecast has not been updated") 
    else: 
        open_file = open(file_name, "wb")
        pickle.dump(parsed_data[0], open_file)
        open_file.close()
        print ("The forecasts have been updated")