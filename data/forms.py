from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField


class SearchRecipeForm(FlaskForm):
    title = StringField(id="title")
    time = IntegerField(id="preparing_time")
    protein = IntegerField(id="protein")
    fats = IntegerField(id="fats")
    carboh = IntegerField(id="carboh")
    submit = SubmitField()


class SearchPlaceForm(FlaskForm):
    title = StringField(id="title")
    adress = StringField(id="adress")
    category = StringField(id="category")
    submit = SubmitField()
