from website.db import orders
from datetime import datetime

def create_order(user, cart):
    orders.insert_one({
        "user": user,
        "items": cart,
        "status": "Placed",
        "created_at": datetime.utcnow()
    })
