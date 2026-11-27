from pymongo import MongoClient

with MongoClient("mongodb://localhost:27017") as client:
    client.admin.command("ping")
    print("Connected to local MongoDB")