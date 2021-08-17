from flask import Flask, render_template, abort, request
import json
from data import data

app = Flask(__name__)  # create a Flask app

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


@app.route('/api/catalog')
def get_catalog():
    return json.dumps(data)


@app.route('/api/catalog', methods=['POST'])
def save_product():
    product = request.get_json()  # Returns a dict
    data.append(product)

    return json.dumps(product)

    # data = request.get_data() #Returns bytes
    # print(data)
    # print(type(data))


@app.route('/api/categories')
def get_categories():
    """
        Get the unique categories from the catalog (data var)
        and return them as a list of string
    """
    categories = []
    for item in data:
        cat = item["category"]
        if cat not in categories:
            categories.append(cat)

    return json.dumps(categories)


@app.route('/api/catalog/id/<id>')
def get_product_by_id(id):

    for product in data:
        if(product["_id"] == id):
            return json.dumps(product)

    abort(404)


@app.route('/api/catalog/category/<category>')
def get_products_by_category(category):
    results = []
    for product in data:
        if(product["category"].lower() == category.lower()):
            results.append(product)

    return json.dumps(results)


@app.route('/api/catalog/cheapest')
def get_cheapest():
    cheapest = data[0]

    for product in data:
        if(product["price"] < cheapest["price"]):
            cheapest = product

    return json.dumps(cheapest)


if __name__ == '__main__':
    app.run(debug=True)
