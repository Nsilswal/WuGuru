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

@bp.route('/fooditems') #search function
def fooditems():
        form = SearchForm()
        fooditems = Fooditem.get_all()
        return render_template('fooditem_home.html', title = "Food Item Home",
        avail_fi = fooditems, form = form)
        #return 'Hello World'

@bp.route('/fooditems/filter/<int:attribute>/<int:ordering>', methods=['GET']) #retrieve all attributes
def fooditems_filter(attribute, ordering):
    fooditems = Fooditem.get_all(attribute, ordering)
    return render_template('fooditem_home.html', title="Food Item Home", avail_fi = fooditems)

@bp.route('/fooditems/search', methods=['GET']) #keyword matching for search
def fooditems_search():
    keyword = request.args.get('query')
    fooditems = Fooditem.search_by_keyword(keyword)
    return render_template('fooditem_home.html', title="Food Item Home", avail_fi = fooditems)

@bp.route('/fooditems/add',methods=['POST']) #adding inputted food item to database
def fooditems_add():
    form = AddForm()
    if form.validate_on_submit():
        restaurantID = current_user.restaurantOwned
        Fooditem.register(form.name.data,form.fats.data,form.protein.data,
        form.sugars.data, form.price.data, form.calories.data, 
        form.allergens.data, restaurantID, form.diet.data)
        return redirect(url_for('fooditems.fooditems'))
    return render_template('add_fooditem.html',title='Add a Menu Item', form = form)

@bp.route('/fooditems/delete',methods=['POST']) #removing inputted food item from database
def fooditems_delete():
    form = DeleteForm()
    if form.validate_on_submit():
        restaurantID = current_user.restaurantOwned
        Fooditem.delete_fi(form.name.data,restaurantID)
        return redirect(url_for('fooditems.fooditems'))
    return render_template('delete_fooditem.html',title='Delete a Menu Item', form = form)        

class SearchForm(FlaskForm): #flask form for searching food items
        title = StringField('Food Item name',validators=[DataRequired()])
        search = SubmitField('Search')

class AddForm(FlaskForm): #flask form for adding a new food item with appropriate categories
        name = StringField('Enter name', validators=[DataRequired()])
        price = FloatField('Price:', validators=[DataRequired()])
        protein = FloatField('Protein (g):', validators=[DataRequired()])
        sugars = FloatField('Sugars:', validators=[DataRequired()])
        fats = FloatField('Fats:', validators=[DataRequired()])
        calories = IntegerField('Calories:', validators=[DataRequired()])
        allergens = StringField('Add allergens:', validators = [DataRequired()])
        diet = StringField('Add dietary restriction')
        submit = SubmitField('Submit')

class DeleteForm(FlaskForm): #flask form for deleting food item, takes only item name
    name = StringField('Enter name', validators=[DataRequired()])
    submit = SubmitField('Submit')