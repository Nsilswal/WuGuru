from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
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





