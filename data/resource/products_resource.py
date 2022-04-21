from flask import jsonify
from flask_restful import Resource, abort
from data.cuisine import Recipe
from data import db_session
from data.products import Product


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        product = session.query(Recipe).all()
        info = product.to_dict()
        return jsonify(info)


class ProductsResource(Resource):
    def get(self, id):
        session = db_session.create_session()
        product = session.query(Product).get(id)
        a = []
        for item in product:
            info = item.to_dict()
            a.append(info)
        return jsonify(a)


def abort_if_recipe_not_found(id):
    session = db_session.create_session()
    recipe = session.query(Product).get(id)
    if not recipe:
        abort(404, message=f"Product with id = {id} not found")
