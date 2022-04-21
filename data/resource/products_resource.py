from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.products import Product


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        product = session.query(Product).all()
        info = []
        for i in product:
            info.append(i.to_dict())
        return jsonify(info)


class ProductsResource(Resource):
    def get(self, id):
        session = db_session.create_session()
        product = session.query(Product).get(id)
        info = product.to_dict()
        return jsonify(info)


def abort_if_recipe_not_found(id):
    session = db_session.create_session()
    recipe = session.query(Product).get(id)
    if not recipe:
        abort(404, message=f"Product with id = {id} not found")
