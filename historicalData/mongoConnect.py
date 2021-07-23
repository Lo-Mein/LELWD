import pymongo
from flask import Flask
from flask_cors import CORS
import datetime
from calendar import monthrange


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

def pie_chart_data(month, days):
    max_data = []
    year = 2015
    data_list = [db.hourly_2015_demand, db.hourly_2016_demand, db.hourly_2017_demand, db.hourly_2018_demand, db.hourly_2019_demand, db.hourly_2020_demand]
    for data in data_list:
        for day in range(1, days+1):
            demand_list = data.find({'Date': datetime.datetime(year, month, day, 4, 0)})
            daily_peak = 0
            for item in demand_list:
                if item['RT_Demand'] > daily_peak:
                    daily_peak = item['RT_Demand']
                    hr_end = item['Hr_End']
            max_data.append(hr_end)
        year += 1
    return max_data


if __name__ == "__main__":
    current_month = datetime.datetime.now().month
    num_days = monthrange(2019,current_month)[1]
    # data2015 = get2015Data(num_days, current_month)
    pie_data = pie_chart_data(current_month, num_days)
    
    
    
