from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime

from .models.fooditem import Fooditem

bp = Blueprint('fooditems',__name__)

@bp.route('/fooditems')
def food_items():
        form = SearchForm()
        food_items = Fooditem.get_all()
        return render_template('fooditem_home.html', title = "Food Item Home",
        avail_fi = food_items, form = form)
        #return 'Hello World'

class SearchForm(FlaskForm):
        title = StringField('Food Item name',validators=[DataRequired()])
        search = SubmitField('Search')

