from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, FloatField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime

from .models.fooditem import Fooditem

bp = Blueprint('fooditems',__name__)

@bp.route('/fooditems')
def fooditems():
        form = SearchForm()
        fooditems = Fooditem.get_all()
        return render_template('fooditem_home.html', title = "Food Item Home",
        avail_fi = fooditems, form = form)
        #return 'Hello World'

@bp.route('/fooditems/filter/<int:attribute>/<int:ordering>', methods=['GET'])
def fooditems_filter(attribute, ordering):
    fooditems = Fooditem.get_all(attribute, ordering)
    return render_template('fooditem_home.html', title="Food Item Home", avail_fi = fooditems)

@bp.route('/fooditems/search', methods=['GET'])
def fooditems_search():
    keyword = request.args.get('query')
    fooditems = Fooditem.search_by_keyword(keyword)
    return render_template('fooditem_home.html', title="Food Item Home", avail_fi = fooditems)

@bp.route('/fooditems/add',methods=['POST'])
def fooditems_add():
    form = AddForm()
    if form.validate_on_submit():
        restuarantID = current_user.restaurantOwned
        Fooditem.register(form.name.data,form.price.data,form.protein.data,
        form.sugars.data, form.fats.data, forms.calories.data, 
        forms.allergens.data, restaurantID, forms.diet.data)
        return redirect(url_for('index.index'))
    return render_template('add_fooditem.html',title='Add a Menu Item', form = form)
    


class SearchForm(FlaskForm):
        title = StringField('Food Item name',validators=[DataRequired()])
        search = SubmitField('Search')

class AddForm(FlaskForm):
        name = StringField('Add name', validators=[DataRequired()])
        protein = FloatField('Protein (g):', validators=[DataRequired()])
        sugars = FloatField('Sugars:', validators=[DataRequired()])
        fats = FloatField('Fats:', validators=[DataRequired()])
        price = FloatField('Price:', validators=[DataRequired()])
        calories = IntegerField('Calories:', validators=[DataRequired()])
        allergens = StringField('Add allergens:', validators = [DataRequired()])
        diet = StringField('Add dietary restriction')
        submit = SubmitField('Submit')


