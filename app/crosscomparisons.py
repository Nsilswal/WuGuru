from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime

from .models.fooditem import Fooditem

bp = Blueprint('crosscomparisons',__name__)

@bp.route('/crosscomparisons')
def cross_comparisons():
    fooditems = Fooditem.get_all()  # Assuming Fooditem.get_all() fetches the food items from your database
    return render_template('crosscomparisons_home.html', title="Cross Comparisons Home", avail_fi=fooditems,)
