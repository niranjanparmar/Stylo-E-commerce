from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stylo_db"]

products = db["products"]
orders = db["orders"]
