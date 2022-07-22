import pymongo
from flask import Flask
from flask_cors import CORS
import datetime
from calendar import monthrange
import numpy as np



connection_url = "mongodb+srv://admin:4z9gadc6vGKvc1TN@lelwd-generator-applica.141qu.mongodb.net/?retryWrites=true&w=majority"
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

# Database
db = client.get_database("historical-data")


# Assign a variable to every differnt collection
hourly_2015_demand = db.hourly_2015_demand

hourly_2016_demand = db.hourly_2016_demand

hourly_2017_demand = db.hourly_2017_demand

hourly_2018_demand = db.hourly_2018_demand

hourly_2019_demand = db.hourly_2019_demand

hourly_2020_demand = db.hourly_2020_demand

hourly_2021_demand = db.hourly_2021_demand



# To insert a single document into the database,
# insert_one() function is used
# @app.route("/insert-one/<name>/<id>/", methods=["GET"])
# def insertOne(name, id):
#     queryObject = {"Name": name, "ID": id}
#     query = SampleTable.insert_one(queryObject)
#     return "Query inserted...!!!"

# use find_one to find a specific document

# gets all 2015 data
def get2015Data(days, month):
    max_data = dict()
    data = db.hourly_2015_demand
    for day in range(1, days + 1):
        demand_list = data.find({"Date": datetime.datetime(2015, month, day, 4, 0)})
        daily_peak = 0
        for item in demand_list:
            if item["RT_Demand"] > daily_peak:
                daily_peak = item["RT_Demand"]
                hr_end = item["Hr_End"]
        max_data[daily_peak] = hr_end
    return max_data


# gets all 2016 data
def get2016Data():
    max_data = dict()
    data = db.hourly_2016_demand
    for day in range(1, days + 1):
        demand_list = data.find({"Date": datetime.datetime(2016, month, day, 4, 0)})
        daily_peak = 0
        for item in demand_list:
            if item["RT_Demand"] > daily_peak:
                daily_peak = item["RT_Demand"]
                hr_end = item["Hr_end"]
        max_data[daily_peak] = hr_end
        return max_data


# gets all 2017 data
def get2017Data():
    data = db.hourly_2017_demand
    max_data = dict()
    for day in range(1, days + 1):
        demand_list = data.find({"Date": datetime.datetime(2017, month, day, 4, 0)})
        daily_peak = 0
        for item in demand_list:
            if item["RT_Demand"] > daily_peak:
                daily_peak = item["RT_Demand"]
                hr_end = item["Hr_end"]
        max_data[daily_peak] = hr_end
        return max_data


# gets all 2018 data
def get2018Data():
    data = db.hourly_2018_demand
    max_data = dict()
    for day in range(1, days + 1):
        demand_list = data.find({"Date": datetime.datetime(2018, month, day, 4, 0)})
        daily_peak = 0
        for item in demand_list:
            if item["RT_Demand"] > daily_peak:
                daily_peak = item["RT_Demand"]
                hr_end = item["Hr_end"]
        max_data[daily_peak] = hr_end
        return max_data


# gets all 2019 data
def get2019Data():
    data = db.hourly_2019_demand
    max_data = dict()
    for day in range(1, days + 1):
        demand_list = data.find({"Date": datetime.datetime(2019, month, day, 4, 0)})
        daily_peak = 0
        for item in demand_list:
            if item["RT_Demand"] > daily_peak:
                daily_peak = item["RT_Demand"]
                hr_end = item["Hr_end"]
        max_data[daily_peak] = hr_end
        return max_data


# gets all 2020 data
def get2020Data():
    max_data = dict()
    data = db.hourly_2020_demand
    for day in range(1, days + 1):
        demand_list = data.find({"Date": datetime.datetime(2020, month, day, 4, 0)})
        daily_peak = 0
        for item in demand_list:
            if item["RT_Demand"] > daily_peak:
                daily_peak = item["RT_Demand"]
                hr_end = item["Hr_end"]
        max_data[daily_peak] = hr_end
        return max_data

def get2021Data():
    max_data = dict()
    data = db.hourly_2021_demand
    for day in range(1, days + 1):
        demand_list = data.find({"Date": datetime.datetime(2021, month, day, 4, 0)})
        daily_peak = 0
        for item in demand_list:
            if item["RT_Demand"] > daily_peak:
                daily_peak = item["RT_Demand"]
                hr_end = item["Hr_end"]
        max_data[daily_peak] = hr_end
        return max_data



def get_monthly_historical_data():
    month = datetime.datetime.now().month
    month_string = datetime.datetime.now().strftime('%b')
    days = monthrange(2019,month)[1]
    max_hour = []
    max_peak = []
    year = 2015
    year_data = [db.hourly_2015_demand, db.hourly_2016_demand, db.hourly_2017_demand, db.hourly_2018_demand, db.hourly_2019_demand, db.hourly_2020_demand, db.hourly_2021_demand]
    for data in year_data:
        for day in range(1, days+1):
            demand_list = data.find({'Date': "{0}-{1}-{2}".format(day, month_string, str(year)[-2:])})
            daily_peak = 0
            for item in demand_list:
                if item['RT_Demand'] > daily_peak:
                    daily_peak = item['RT_Demand']
                    hr_end = item['Hr_End']
            max_hour.append(hr_end)
            max_peak.append(daily_peak)
        year += 1
    return max_hour, max_peak

def update_current_month_threshold(threshold):
    data = db.current_month_threshold
    data.update_one({}, {"$set": {"current_month_threshold": threshold}})


if __name__ == "__main__":
    # max_hour, max_peak = get_monthly_historical_data()

    update_current_month_threshold(18049)
