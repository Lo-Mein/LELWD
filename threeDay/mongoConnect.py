import pymongo
from flask import Flask
from flask_cors import CORS
import datetime
from calendar import monthrange
import numpy as np
# from threeDayForecast import retrieve_actual_data


connection_url = "mongodb+srv://RyanMatt:JeffKramer1@historicaldata.2fqkr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

# Database
db = client.get_database("lelwd")


# Assign a variable to every differnt collection
hourly_2015_demand = db.hourly_2015_demand

hourly_2016_demand = db.hourly_2016_demand

hourly_2017_demand = db.hourly_2017_demand

hourly_2018_demand = db.hourly_2018_demand

hourly_2019_demand = db.hourly_2019_demand

hourly_2020_demand = db.hourly_2020_demand


count = hourly_2015_demand.count_documents({})


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
    for day in range(1, days+1):
        demand_list = data.find({'Date': datetime.datetime(2015, month, day, 4, 0)})
        daily_peak = 0
        for item in demand_list:
            if item['RT_Demand'] > daily_peak:
                daily_peak = item['RT_Demand']
                hr_end = item['Hr_End']
        max_data[daily_peak] = hr_end
    return max_data
        


# gets all 2016 data
def get2016Data():
    data = db.hourly_2016_demand
    demand_list = data.find()
    for item in demand_list:
        print(item)
        return item
        


# gets all 2017 data
def get2017Data():
    data = db.hourly_2017_demand
    demand_list = data.find()
    for item in demand_list:
        print(item)


# gets all 2018 data
def get2018Data():
    data = db.hourly_2018_demand
    demand_list = data.find()
    for item in demand_list:
        print(item)


# gets all 2019 data
def get2019Data():
    data = db.hourly_2019_demand
    demand_list = data.find()
    for item in demand_list:
        print(item)


# gets all 2020 data
def get2020Data():
    data = db.hourly_2020_demand
    demand_list = data.find()
    for item in demand_list:
        print(item)


def get_monthly_historical_data():
    month = datetime.datetime.now().month
    days = monthrange(2019,month)[1]
    max_hour = []
    max_peak = []
    year = 2015
    year_data = [db.hourly_2015_demand, db.hourly_2016_demand, db.hourly_2017_demand, db.hourly_2018_demand, db.hourly_2019_demand, db.hourly_2020_demand]
    for data in year_data:
        for day in range(1, days+1):
            demand_list = data.find({'Date': datetime.datetime(year, month, day, 4, 0)})
            daily_peak = 0
            for item in demand_list:
                if item['RT_Demand'] > daily_peak:
                    daily_peak = item['RT_Demand']
                    hr_end = item['Hr_End']
            max_hour.append(hr_end)
            max_peak.append(daily_peak)
        year += 1
    return max_hour, max_peak


if __name__ == "__main__":
    # pie_data, threshold_data = get_monthly_historical_data()
    # print(np.percentile(threshold_data, 75))
    # d = datetime.date.today()
    # month_data = []
    # for day in range(1, d.day):
    #     api_date = '{}{:02d}{:02d}'.format(d.year,d.month, day)
    #     api_data = retrieve_actual_data(api_date)
    #     day_peak = float(0)
    #     for i in range(23):
    #         day_data = float(api_data[i]['Load'])
    #         if day_data > day_peak:
    #             day_peak = day_data
    #     month_data.append(day_peak)
    
    # print(max(month_data) * .97)
    pass

    
    
    
    
