import pymongo
from flask import Flask
from flask_cors import CORS


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
print(count)

# To insert a single document into the database,
# insert_one() function is used
# @app.route("/insert-one/<name>/<id>/", methods=["GET"])
# def insertOne(name, id):
#     queryObject = {"Name": name, "ID": id}
#     query = SampleTable.insert_one(queryObject)
#     return "Query inserted...!!!"

# use find_one to find a specific document

# gets all 2015 data
def get2015Data():
    data = db.hourly_2015_demand
    demand_list = data.find()
    for item in demand_list:
        print(item)
        return item


# gets all 2016 data
def get2016Data():
    data = db.hourly_2016_demand
    demand_list = data.find()
    for item in demand_list:
        print(item)


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


if __name__ == "__main__":
    data2015 = get2015Data()
