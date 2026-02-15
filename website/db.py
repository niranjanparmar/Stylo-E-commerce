from pymongo import MongoClient

client = MongoClient("mongodb+srv://parmarniranjan15_db_user:Stylo1234@cluster0.ngtydeh.mongodb.net/stylo_db?retryWrites=true&w=majority")
db = client["stylo_db"]

products = db["products"]
orders = db["orders"]
