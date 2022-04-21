import os
from flask import Flask, render_template
from data import db_session
from data.resource import cuisine_resource, products_resource
from flask_restful import Api

# Initialization
db_session.global_init("db/kastybiy.db")
app = Flask(__name__)
app.config["SECRET_KEY"] = "dvrQYr4v62d"

# Api initialization
api = Api(app)
api.add_resource(cuisine_resource.CuisineListResource, "/api/get/cuisine")
api.add_resource(cuisine_resource.CuisineResource, "/api/get/cuisine/<id>")
api.add_resource(cuisine_resource.CuisineCategoryResource, "/api/get/cuisine/<category>")

api.add_resource(products_resource.ProductsResource, "/api/get/products/<id>")
api.add_resource(products_resource.ProductsListResource, "/api/get/products")


@app.route("/", methods=["GET"])
def base():
    return render_template("base.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/cuisine")
def cuisine():
    return render_template("cuisine.html")


@app.route("/culture")
def culture():
    return render_template("card.html")


@app.route("/places")
def places():
    return render_template("places.html")


if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
