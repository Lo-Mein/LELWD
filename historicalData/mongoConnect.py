import pymongo
from flask import Flask
from flask_cors import CORS


connection_url = "mongodb+srv://RyanMatt:JeffKramer1@historicaldata.2fqkr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database("HistoricalData")

# Table
SampleTable = Database.SampleTable

# To insert a single document into the database,
# insert_one() function is used
@app.route("/insert-one/<name>/<id>/", methods=["GET"])
def insertOne(name, id):
    queryObject = {"Name": name, "ID": id}
    query = SampleTable.insert_one(queryObject)
    return "Query inserted...!!!"


def get2015Data():
    # data = db.2015_hourly_demand
    demand_list = data.find()
    for item in demand_list:
        print(item)


# if __name__ == "__main__":
# data = get2015Data()
