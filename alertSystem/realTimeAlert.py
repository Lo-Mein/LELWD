import requests
from requests.models import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xmltodict
import datetime
import doAlert


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_real_time_load():
    real_time_api = "https://webservices.iso-ne.com/api/v1.1/fiveminutesystemload/current"
    response = requests.get(
        real_time_api,
        auth=HTTPBasicAuth("info.rmsolutionss@gmail.com", "JeffKramer1"),
        verify=False,
    )

    xml_data = response.content
    xml_dict = xmltodict.parse(xml_data)

    return xml_dict["FiveMinSystemLoad"]["NativeLoad"]


def get_forecast_load():
    d = datetime.date.today()
    api_date = "{}{:02d}{:02d}".format(d.year, d.month, d.day)
    forecast_api = "https://webservices.iso-ne.com/api/v1.1/hourlyloadforecast/day/{}".format(
        api_date)
    response = requests.get(
        forecast_api,
        auth=HTTPBasicAuth("info.rmsolutionss@gmail.com", "JeffKramer1"),
        verify=False,
    )

    xml_data = response.content
    xml_dict = xmltodict.parse(xml_data)

    time = datetime.datetime.now().hour

    return xml_dict["HourlyLoadForecasts"]["HourlyLoadForecast"][time]["LoadMw"]


def send_alert(real_load, forecasted_load):
    alert = False
    if real_load - forecasted_load > 1000:
        alert = True

    return alert


if __name__ == "__main__":
    real_time_load = round(float(get_real_time_load()))
    forecasted_load = int(get_forecast_load())

    alert = send_alert(real_time_load, forecasted_load)

    if alert:
        load_alert = real_time_load - forecasted_load
        body = """\
        <html>
            <head>
                <meta charset="UTF-8">
                <link rel='stylesheet' type='text/css' media='screen' href='df_style.css'>
            </head>
            <body>
                <p style="font-family: Verdana; font-size: 14px;">	
                    The current load is: <b>{0}</b>. Exceeding the forecast by: <b>{1}</b>.
                </p>
            </body>
        </html>
        """.format(
            real_time_load,
            load_alert
        )
        doAlert.send_alert(body, "Load Alert")
