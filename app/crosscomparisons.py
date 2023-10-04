from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
from flask import current_app as app

from .models.fooditem import Fooditem

bp = Blueprint('crosscomparisons',__name__)

@bp.route('/crosscomparisons')
def cross_comparisons():
    fooditems = Fooditem.get_all()  # Assuming Fooditem.get_all() fetches the food items from your database
    return render_template('crosscomparisons_home.html', title="Cross Comparisons Home", avail_fi=fooditems,)

# @bp.route('/crosscomparisons/compare/<string:fd1>/<string:fd2>/<string:category>/<string:method>', methods=['GET'])
# def compare(fd1, fd2,category,method):
#     return ("comparing " + fd1 + " and " + fd2 + " in category " + category + " using method " + method)

@bp.route('/crosscomparisons/compare', methods=['POST'])
def compare():
    comparison_result = None

    if request.method == 'POST':
        # Get form data from the request
        food1 = request.form.get('food1')
        food2 = request.form.get('food2')
        category = request.form.get('category')
        comparison = request.form.get('comparison')
        order = comparison

        if comparison == "most":
            comparison = "DESC"
        else:
            comparison = "ASC"


        # Construct the SQL query dynamically based on the category and comparison type
        query = f"SELECT * FROM fooditems WHERE name IN ('{food1}', '{food2}') ORDER BY {category} {comparison} LIMIT 1"
    
        # Execute the query using your database connection and fetch the result
        row = app.db.execute(query)
        comparison_result = f'The food with the {order} {category} are {row[0][1]}'

    # Render the template with comparison_result
    # return row[0][1]
    return render_template('crosscomparisons_home.html', comparison_result=comparison_result)
