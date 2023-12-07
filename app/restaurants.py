from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TimeField
from wtforms.validators import DataRequired
from datetime import datetime
 
from .models.restaurant import Restaurants

bp = Blueprint('restaurants', __name__)

@bp.route('/restaurants')
def restaurants():
    restaurants = Restaurants.get_all()
    return render_template('restaurant.html', title="WU Restaurants", avail_rests = restaurants)

@bp.route('/restaurants/filter/<int:attribute>/<int:ordering>', methods=['GET'])
def restaurants_filter(attribute, ordering):
    restaurants = Restaurants.get_all(attribute, ordering)
    return render_template('restaurant.html', title="WU Restaurants", avail_rests = restaurants)

'''
@bp.route('/restaurants/menu/<int:id>', methods=['GET'])
def restaurants_menu(id):
    menu = Restaurants.get_menu(id)
    return render_template('restaurant.html', title="Menu", avail_recs = menu)

'''

#Create a form that can be used by restaurant owners to modify current restaurant attributes
@bp.route('/restaurant_edit', methods=['POST'])
def Rest_Edit():
    form = Restaurant_EditForm()
    if form.validate_on_submit():
        Restaurants.edit(form.floor.data,
                         form.MobileOrder.data,
                         form.OpeningTime.data,
                         form.ClosingTime.data, current_user.restaurantOwned)
        flash('Edits have been processed!')
        return redirect(url_for('restaurants.restaurants'))
    return render_template('restaurant_edit.html', title='Edit Restaurant Info', form=form)

class Restaurant_EditForm(FlaskForm):
    floor = IntegerField('Floor:')
    MobileOrder = IntegerField('Mobile Order (Enter 0 for No and 1 for Yes):')
    OpeningTime = TimeField('Opening Time:')
    ClosingTime = TimeField('Closing Time')
    submit = SubmitField('Edit')

