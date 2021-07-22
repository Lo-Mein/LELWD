import pymongo

try:
    client = pymongo.MongoClinet(
        "mongodb+srv://RyanMatt:<password>@historicaldata.2fqkr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    print("connection established")
except:
    print("error")