import os
from flask import Flask, render_template, request, make_response
from flask_wtf import form
from werkzeug.utils import redirect

from data import db_session
from data.cuisine import Recipe
from data.products import Product
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


@app.route("/", methods=["GET", "POST"])
def base():
    if request.method == "POST":
        id = request.form.get('btn')
        res = make_response(redirect(f"/cuisine"))
        favorite = eval(getFavoriteCookie())
        if id in favorite:
            del favorite[favorite.index(id)]
        else:
            favorite.append(id)
        print(favorite)
        res.set_cookie("favorite", f"{favorite}", 60 * 60 * 24 * 15)
        return res
    db_sess = db_session.create_session()
    data = db_sess.query(Recipe).all()
    fridge = eval(getFridgeCookie())
    favorite = eval(getFavoriteCookie())
    recipes = []
    s = []
    for i in data:
        d = i.to_dict()
        d['favorite'] = 1 if str(d['id']) in favorite else 0
        q = d['itogProducts'].split("*")
        cnt = 0
        for t in fridge:
            if fridge[t] == 1 and str(t) in q:
                cnt += 1
        coeff = round(cnt / len(q) * 100, 1)
        d['cookPosibility'] = coeff
        s.append(d)
        if len(s) == 4:
            recipes.append(s)
            s = []
    if len(s) < 4:
        recipes.append(s)
    return render_template("cuisine.html", recipes=recipes)


@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/cuisine", methods=["GET", "POST"])
def cuisine():
    if request.method == "POST":
        id = request.form.get('btn')
        res = make_response(redirect(f"/cuisine"))
        favorite = eval(getFavoriteCookie())
        if id in favorite:
            del favorite[favorite.index(id)]
        else:
            favorite.append(id)
        print(favorite)
        res.set_cookie("favorite", f"{favorite}", 60 * 60 * 24 * 15)
        return res
    db_sess = db_session.create_session()
    data = db_sess.query(Recipe).all()
    fridge = eval(getFridgeCookie())
    favorite = eval(getFavoriteCookie())
    recipes = []
    s = []
    for i in data:
        d = i.to_dict()
        d['favorite'] = 1 if str(d['id']) in favorite else 0
        q = d['itogProducts'].split("*")
        cnt = 0
        for t in fridge:
            if fridge[t] == 1 and str(t) in q:
                cnt += 1
        coeff = round(cnt / len(q) * 100, 1)
        d['cookPosibility'] = coeff
        s.append(d)
        if len(s) == 4:
            recipes.append(s)
            s = []
    if len(s) < 4:
        recipes.append(s)
    return render_template("cuisine.html", recipes=recipes)


@app.route('/getfridge')
def getFridgeCookie():
   cookies = request.cookies.get("fridge")
   if cookies is None:
       products = {}
       for i in range(1, 38):
           products[i] = 0
       cookies = f"{products}"
   return cookies


@app.route('/getfavorite')
def getFavoriteCookie():
   cookies = request.cookies.get("favorite")
   if cookies is None:
       cookies = "[]"
   return cookies


@app.route("/recipe/<int:id>", methods=["GET", "POST"])
def recipe(id):
    if request.method == "POST":
        res = make_response(redirect(f"/recipe/{id}"))
        favorite = eval(getFavoriteCookie())
        if str(id) in favorite:
            del favorite[favorite.index(str(id))]
        else:
            favorite.append(str(id))
        res.set_cookie("favorite", f"{favorite}", 60 * 60 * 24 * 15)
        return res
    db_sess = db_session.create_session()
    data = db_sess.query(Recipe).filter(Recipe.id == id).all()[0].to_dict()
    fridge = eval(getFridgeCookie())
    favorite = eval(getFavoriteCookie())
    cnt = 0
    q = data['itogProducts'].split("*")
    for i in fridge:
        if fridge[i] == 1 and str(i) in q:
            cnt += 1
    coeff = round(cnt / len(q) * 100, 1)
    data['cookPosibility'] = coeff
    data['cookSteps'] = data['cookSteps'].split("\\n")
    data['products'] = ", ".join(data['products'].split("*")[1:])
    if str(id) in favorite:
        data['favorite'] = 1
    else:
        data['favorite'] = 0

    return render_template("recipe.html", recipe=data)


@app.route("/fridge", methods=["GET", "POST"])
def fridge():

    productsDict = {}
    if request.method == "POST":
        res = make_response(redirect("/fridge"))
        products = {}
        for i in range(1, 38):
            products[i] = 1 if request.form.get(f"{i}") == "1" else 0
        res.set_cookie("fridge", f"{products}", 60 * 60 * 24 * 15)
        return res
    db_sess = db_session.create_session()
    data = db_sess.query(Product).all()
    t = []
    products = []
    fridge = eval(getFridgeCookie())
    print(fridge)
    for i in data:
        d = i.to_dict()
        d['inFridge'] = fridge[d['id']]
        print(d)
        t.append(d)
        if len(t) == 4:
            products.append(t)
            t = []
    return render_template("fridge.html", products=products)


@app.route("/favorite", methods=["GET", "POST"])
def favorite():
    if request.method == "POST":
        id = request.form.get('btn')
        res = make_response(redirect(f"/favorite"))
        favorite = eval(getFavoriteCookie())
        if id in favorite:
            del favorite[favorite.index(id)]
        else:
            favorite.append(id)
        res.set_cookie("favorite", f"{favorite}", 60 * 60 * 24 * 15)
        return res
    fridge = eval(getFridgeCookie())
    favorite = eval(getFavoriteCookie())
    db_sess = db_session.create_session()
    data = db_sess.query(Recipe).all()
    recipes = []
    s = []
    print(fridge)
    for i in data:
        d = i.to_dict()
        if str(d['id']) in favorite:
            d['favorite'] = 1
            q = d['itogProducts'].split("*")
            cnt = 0
            for t in fridge:
                if fridge[t] == 1 and str(t) in q:
                    cnt += 1
            coeff = round(cnt / len(q) * 100, 1)
            d['cookPosibility'] = coeff
            s.append(d)
        else:
            d['favorite'] = 0
        if len(s) == 4:
            recipes.append(s)
            s = []
    recipes.append(s)
    return render_template("cuisine.html", recipes=recipes)


if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
