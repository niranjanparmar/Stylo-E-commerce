from website.db import products
from bson import ObjectId


def get_all_products():
    return list(products.find())


def get_product_by_id(product_id):
    return products.find_one({"_id": ObjectId(product_id)})


def create_product(name, price, image, stock):
    products.insert_one({
        "name": name,
        "price": price,
        "image": image,
        "stock": stock
    })
