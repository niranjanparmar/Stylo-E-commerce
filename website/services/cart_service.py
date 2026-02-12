from website.services.product_service import get_product_by_id
from flask import session


def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session["cart"] = cart


def remove_from_cart(product_id):
    cart = session.get("cart", {})
    if product_id in cart:
        del cart[product_id]
    session["cart"] = cart


def get_cart_items():
    cart = session.get("cart", {})
    items = []

    for product_id, qty in cart.items():
        product = get_product_by_id(product_id)
        if product:
            product["qty"] = qty
            items.append(product)

    return items
