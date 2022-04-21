from flask import jsonify
from flask_restful import Resource, abort
from data.cuisine import Recipe
from data import db_session


class CuisineResource(Resource):
    def get(self, id: int):
        abort_if_recipe_not_found(id)
        session = db_session.create_session()
        recipe = session.query(Recipe).get(id)
        info = recipe.to_dict()
        return jsonify(info)


class CuisineCategoryResource(Resource):
    def get(self, category: str):
        session = db_session.create_session()
        recipes = session.query(Recipe).filter(Recipe.category_global == category).all()
        a = []
        for item in recipes:
            info = item.to_dict()
            a.append(info)
        return jsonify(a)


class CuisineListResource(Resource):
    def get(self):
        session = db_session.create_session()
        recipes = session.query(Recipe).all()
        a = []
        for item in recipes:
            info = item.to_dict()
            a.append(info)
        return jsonify(a)


def abort_if_recipe_not_found(id):
    session = db_session.create_session()
    recipe = session.query(Recipe).get(id)
    if not recipe:
        abort(404, message=f"Recipe with id = {id} not found")

