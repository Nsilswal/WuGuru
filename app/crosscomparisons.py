from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
from flask import current_app as app

from .models.food_comparison import FoodComparison

bp = Blueprint('crosscomparisons',__name__)

@bp.route('/crosscomparisons')
def cross_comparisons():
    topComps = FoodComparison.getTop5()
    return render_template('crosscomparisons_home.html', title="Cross Comparisons Home", top_comparisons=topComps)

@bp.route('/crosscomparisons/compare', methods=['POST'])
def compare():
    comparison_result = None

    query = "SELECT r.name AS restaurant_name, AVG(reviews.rating) AS average_rating FROM restaurants r JOIN reviews ON r.id = reviews.restaurant_id GROUP BY r.name ORDER BY average_rating DESC;"
    avgReviews = app.db.execute(query)
    avgReviews = [(restaurant, round(average_rating, 2)) for restaurant, average_rating in avgReviews]

    ratio1 = request.form.get('ratio1')
    ratio2 = request.form.get('ratio2')
    print(ratio1)
    print(ratio2)

    if request.method == 'POST':
        # Get form data from the request
        food1 = request.form.get('food1')
        food2 = request.form.get('food2')

        FoodComparison.add_or_increment(food1, food2)

        categories = request.form.getlist('categories[]')  # Use getlist to handle multiple selected categories
        comparison = request.form.get('comparison')
        order = comparison

        if comparison == "most":
            comparison = "DESC"
        else:
            comparison = "ASC"

        # Construct the SQL query dynamically based on the categories and comparison type
        # For simplicity, assume the user wants to compare all selected categories

        if ratio1 != "None" and ratio2 != "None":
        # Construct the SQL query to order by ratio1 / ratio2 in descending order (highest ratio first)
            query = f"SELECT * FROM fooditems WHERE name IN ('{food1}', '{food2}') ORDER BY {ratio1} / {ratio2} DESC LIMIT 1"
            categories_string = f'{ratio1} / {ratio2}'
        else:
        # Construct the SQL query based on the selected categories and comparison type
            categories_string = f' {comparison} ,'.join(categories)
            print("categories_string: ", categories_string)
            query = f"SELECT * FROM fooditems WHERE name IN ('{food1}', '{food2}') ORDER BY {categories_string} {comparison}"

        # Execute the query using your database connection and fetch the result
        row = app.db.execute(query)
        print(row)
        
        # Checking query results
        categories_string = categories_string.replace("DESC", "").replace("ASC", "").replace(",", " and ")

        if len(row) == 0:
            comparison_result = f"Sorry, we couldn't find any food items with the names {food1} and {food2}"
        else:
            comparison_result = f'The food with the {order} {categories_string} is {row[0][1]}'

    # Render the template with comparison_result
    topComps = FoodComparison.getTop5()
    return render_template('crosscomparisons_home.html', comparison_result=comparison_result,top_comparisons=topComps)


@bp.route('/foodcomparisons/addOrIncrement', methods=['GET'])
def add_or_increment():
    # Get food1 and food2 from the query parameters
    food1 = request.args.get('food1')
    food2 = request.args.get('food2')
    
    ret = FoodComparison.add_or_increment(food1, food2)
    
    print(FoodComparison.search_by_keyword(food1))
    
    # You can return some data or a template if needed
    return render_template('crosscomparisons_home.html')

