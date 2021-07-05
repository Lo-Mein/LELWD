import requests
import json
from requests.models import HTTPBasicAuth


def retrieveData():
    sevenDayAPI = "https://webservices.iso-ne.com/api/v1.1/sevendayforecast/current.json"
    response = requests.get(sevenDayAPI, auth=HTTPBasicAuth(
        'info.rmsolutionss@gmail.com', 'JeffKramer1'))
    json_data = response.json()
    day_data = json_data.get("SevenDayForecasts")
    print(day_data["SevenDayForecast"][0]["MarketDay"][0])


if __name__ == "__main__":
    retrieveData()
