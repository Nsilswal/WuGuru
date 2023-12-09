from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
from flask import current_app as app

from flask import send_file
import matplotlib.pyplot as plt
from io import BytesIO

from .models.food_comparison import FoodComparison
from .models.fooditem import Fooditem

bp = Blueprint('crosscomparisons',__name__)

# Endpoint for the crosscomparisons home page
@bp.route('/crosscomparisons')
def cross_comparisons():
    topComps = FoodComparison.getTop5()
    return render_template('crosscomparisons_home.html', title="Cross Comparisons Home", top_comparisons=topComps)

# Endpoint to handle the comparison form submission
@bp.route('/crosscomparisons/compare', methods=['POST'])
def compare():
    comparison_result = None

    ratio1 = request.form.get('ratio1')
    ratio2 = request.form.get('ratio2')
    print(ratio1)
    print(ratio2)

    if request.method == 'POST':
        # Get form data from the request
        food1 = request.form.get('food1')
        food2 = request.form.get('food2')

        

        categories = request.form.getlist('categories[]')  # Use getlist to handle multiple selected categories

        # Preventing SQL injections
        validCategories = {"calories", "price", "protein", "sugars", "fats", "Calories", "Price", "Protein", "Sugars", "Fats"}

        for category in categories:
            if category not in validCategories:
                return "Invalid categories", 400
        
        comparison = request.form.get('comparison')
    
        validComparisons = {"most","least","Most","Least"}

        order = comparison
  
        if comparison not in validComparisons:
            return "Invalid comparison type", 400

        if comparison == "most":
            comparison = "DESC"
        else:
            comparison = "ASC"

        # Construct the SQL query dynamically based on the categories and comparison type
        # For simplicity, assume the user wants to compare all selected categories
        rows = ""
        if ratio1 != "None" and ratio2 != "None":
            rows = app.db.execute('''
            SELECT *
            FROM fooditems
            WHERE name IN (:food1,:food2)
            ORDER BY '''+f'{ratio1}/{ratio2} '+
            'DESC'
            , food1=food1,food2=food2,ratio1=ratio1,ratio2=ratio2)

            categories_string = f'{ratio1} / {ratio2}'
        else:
            categories_string = f' {comparison}, '.join(categories)
            categories_string += f' {comparison}'

            query = f'ORDER BY {categories_string}'
            
            rows = app.db.execute('''SELECT *
                                FROM fooditems
                                WHERE name IN (:food1,:food2) ''' + query,
                                food1=food1,food2=food2,categories_string=categories_string)
        
        categories_string = categories_string.replace("DESC", "").replace("ASC", "").replace(",", " and ")

        FoodComparison.add_or_increment(food1, food2)

        if len(rows) == 0:
            comparison_result = f"Sorry, we couldn't find any food items with the names {food1} and {food2}"
        else:
            comparison_result = f'The food with the {order} {categories_string} is {rows[0][1]}'

    # Render the template with comparison_result
    topComps = FoodComparison.getTop5()
    return render_template('crosscomparisons_home.html', comparison_result=comparison_result,top_comparisons=topComps)


# Endpoint to handle the scatterplot form submission and generate plots
@bp.route('/scatterplot', methods=['POST'])
def scatterplot():
    # Get selected categories from the form
    category1 = request.form.get('scatterCategory1')
    category2 = request.form.get('scatterCategory2')

    print(category1)
    print(category2)

    # Check if the categories are valid - make sure no SQL injection is possible
    valid_categories = ['calories', 'price','protein','sugar','fats']  
    if category1 not in valid_categories or category2 not in valid_categories:
        return "Invalid categories", 400

    # Fetch data from the database using parameterized query
    query = f"""SELECT 
                    fooditems.{category1}, fooditems.{category2}
                FROM 
                    fooditems"""

    # Use parameterized query to prevent SQL injection
    rows = app.db.execute(query)
    food_items = [row for row in rows]

    # Extract data for the selected categories, association is maintained through indexing of the list
    x_data = [item[0] for item in food_items]
    y_data = [item[1] for item in food_items]

    # Create a scatterplot using Matplotlib
    plt.scatter(x_data, y_data)
    plt.title(f'Scatterplot of {category1} vs {category2}')
    plt.xlabel(category1)
    plt.ylabel(category2)

    # Save the plot to a BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Clear the Matplotlib figure
    plt.clf()

    # Return the scatterplot image as a response
    return send_file(buffer, mimetype='image/png')


