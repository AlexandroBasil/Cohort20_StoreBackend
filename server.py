from flask import Flask, render_template, abort, request
import json
from data import data
from flask_cors import CORS
from config import db, parse_json

app = Flask(__name__)  # create a Flask app
CORS(app)

me = {
    "name": "Alexandro",
    "last_name": "Garcia",
    "age": 27,
    "address": {
        "street": "Elm Avenue",
        "number": 666
    },
    "email": "agarcia@python.com"
}


@app.route('/')
@app.route('/home')
def home_page():
    return render_template("index.html")


@app.route('/about')
def about_page():
    return me["name"] + " " + me["last_name"]


@app.route('/about/email')
def about_email():
    return me["email"]

# ----------------- CATALOG ------------------------------ #


@app.route('/api/catalog')
def get_catalog():
    cursor = db.products.find({})  # FIRST EXAMPLE
    prods = []
    for prod in cursor:
        prods.append(prod)

    # prods = [prod for prod in cursor] ==> PYTHON WAY
    return parse_json(prods)


@app.route('/api/catalog', methods=['POST'])
def save_product():
    product = request.get_json()  # Returns a dict

    # validations
    if not "title" in product:
        return parse_json({"Error": "title is required", "success": False})

    if not "price" in product or not product["price"]:
        return parse_json({"Error": "price is required and should not be 0", "success": False})

    db.products.insert_one(product)
    return parse_json(product)

    # data = request.get_data() #Returns bytes
    # print(data)
    # print(type(data))


@app.route('/api/categories')
def get_categories():
    """
        Get the unique categories from the catalog (data var)
        and return them as a list of string
    """
    cursor = db.products.find({})
    categories = []
    for item in cursor:
        cat = item["category"]
        if cat not in categories:
            categories.append(cat)

    return parse_json(categories)


@app.route('/api/catalog/id/<id>')
def get_product_by_id(id):
    product = db.products.find_one({"id": id})
    if not product:
        abort(404)

    return parse_json(product)


@app.route('/api/catalog/category/<category>')
def get_products_by_category(category):
    cursor = db.products.find({"category": category})
    results = []
    for product in cursor:
        if(product["category"].lower() == category.lower()):
            results.append(product)

    return parse_json(results)


@app.route('/api/catalog/cheapest')
def get_cheapest():
    cheapest = data[0]

    for product in data:
        if(product["price"] < cheapest["price"]):
            cheapest = product

    return parse_json(cheapest)

# ----------------- POPULATE CATALOG DATABASE ------------------------------ #


@app.route('/api/test/populatedb')
def populate_db():
    for prod in data:
        db.products.insert_one(prod)

    return "Data Loaded"

# ----------------- COUPON CODES ------------------------------ #


@app.route('/api/couponCodes', methods=['POST'])
def save_coupon():
    coupon = request.get_json()

    # VALIDATIONS
    if not "code" in coupon:
        return parse_json({"Error": "code is required", "success": False})

    if not "discount" in coupon or not coupon["discount"]:
        return parse_json({"Error": "discount is required and shouldn't be zero", "success": False})

    db.couponCodes.insert_one(coupon)
    return parse_json(coupon)


@app.route('/api/couponCodes')
def get_coupons():
    cursor = db.couponCodes.find({})
    codes = [code for code in cursor]
    return parse_json(codes)


@app.route('/api/couponCodes/<code>')
def get_coupon(code):
    code = db.couponCodes.find_one({"code": code})
    return parse_json(code)


# ----------------- ORDERS ------------------------------ #
@app.route('/api/orders', methods=['POST'])
def save_order():
    order = request.get_json()

    # VALIDATIONS
    prods = order["products"]
    count = len(prods)
    if (count < 1):
        abort(400, "Error: Missing products, not allowed!")

    total = 0
    for item in prods:
        id = item["_id"]
        print(id)

        db_item = db.products.find_one({"_id": id})
        item["price"] = db_item["price"]
        total += db_item["price"] * item["quantity"]

    print("The total is: ", total)
    order["total"] = total

    if "coupon" in order and order["coupon"]:
        code = order["coupon"]
        coupon = db.couponCodes.find_one({"code": code})
        if coupon:
            discount = coupon["discount"]
            total = total - (total * discount) / 100
            order["total"] = total
        else:
            order["coupon"] = "INVALID"

    db.orders.insert_one(order)
    return parse_json(order)


@app.route('/api/orders')
def get_orders():
    cursor = db.orders.find({})
    orders = [order for order in cursor]
    return parse_json(orders)


@app.route('/api/orders/<userId>')
def get_order_for_user(userId):
    cursor = db.orders.find({"userId": userId})
    orders = [order for order in cursor]
    return parse_json(orders)


# ----------------- APP START ------------------------------ #
if __name__ == '__main__':
    app.run(debug=True)
# ---------------------------------------------------------------- #
# coupon codes
# db.couponCodes
# code, discount

# create a GET to read all
# create a POST to add
# create a GET to search by code
