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

class SearchForm(FlaskForm):
        title = StringField('Food Item name',validators=[DataRequired()])
        search = SubmitField('Search')

