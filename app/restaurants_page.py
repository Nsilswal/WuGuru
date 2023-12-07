from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
 
from .models.restaurant_pages import Restaurant_page

bp = Blueprint('restaurants_page', __name__)


@bp.route('/restaurants_page/<int:id>', methods=['GET'])
def restaurants_page(id):
    restaurant = Restaurant_page.get(id)
    return render_template('restaurants_page.html', title=restaurant.name, avail_rests = restaurant)





