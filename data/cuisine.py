import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "recipes"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cookSteps = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cookTime = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    source = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    calories = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    products = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    proteins = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    fats = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    carboh = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
