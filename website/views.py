from flask import Blueprint, render_template, request, redirect, url_for, session
from website.services.product_service import (
    create_product,
    get_all_products,
    get_product_by_id
)

views = Blueprint("views", __name__)

# ---------------- HOME ----------------
@views.route("/")
def home():
    return render_template(
        "home.html",
        user=session.get("user")
    )

# ---------------- PRODUCTS / SHOP ----------------
@views.route("/products")
def products():
    all_products = get_all_products()
    return render_template(
        "shop.html",
        products=all_products,
        user=session.get("user")
    )
# ---------------- Order confirme --------------
@views.route("/confirme")
def confirme():
    session.pop("cart", None)
    session.modified = True
    return render_template(
        "confirme.html",
        user=session.get("user")
    )

# ---------------- ADD PRODUCT (DEV ONLY) ----------------
@views.route("/add-product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        price = int(request.form.get("price"))
        image = request.form.get("image")
        stock = int(request.form.get("stock"))

        create_product(name, price, image, stock)
        return redirect(url_for("views.products"))

    return render_template(
        "add_product.html",
        user=session.get("user")
    )

# ---------------- ADD TO CART ----------------
@views.route("/add-to-cart/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    qty = int(request.form.get("quantity", 1))

    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]
    cart[product_id] = cart.get(product_id, 0) + qty

    session["cart"] = cart
    session.modified = True

    # 👇 user wahi rahega (shop page)
    return redirect(request.referrer)

# ---------------- VIEW CART ----------------
@views.route("/cart")
def cart():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    cart = session.get("cart", {})
    cart_items = []
    grand_total = 0

    for product_id, qty in cart.items():
        product = get_product_by_id(product_id)
        if not product:
            continue

        item_total = product["price"] * qty
        grand_total += item_total

        cart_items.append({
            "_id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "image": product["image"],
            "quantity": qty,
            "total": item_total
        })

    return render_template(
        "cart.html",
        products=cart_items,
        total=grand_total,
        user=session.get("user")
    )

# ---------------- CHECKOUT / BILL ----------------
@views.route("/checkout")
def checkout():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    cart = session.get("cart", {})
    bill_items = []
    grand_total = 0

    for product_id, qty in cart.items():
        product = get_product_by_id(product_id)
        if not product:
            continue

        total_price = product["price"] * qty
        grand_total += total_price

        bill_items.append({
            "name": product["name"],
            "price": product["price"],
            "quantity": qty,
            "total": total_price
        })

    return render_template(
        "bill.html",
        products=bill_items,
        total=grand_total,
        user=session.get("user")
    )

# ---------------- REMOVE FROM CART ----------------
@views.route("/remove-from-cart/<product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})

    if product_id in cart:
        del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("views.cart"))

