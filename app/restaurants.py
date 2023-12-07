from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TimeField
from wtforms.validators import DataRequired
from datetime import datetime
 
from .models.restaurant import Restaurants
from .models.review import Review
from .models.fooditem import Fooditem
from .models.restaurant_photo import RestaurantPhotos

bp = Blueprint('restaurants', __name__)

@bp.route('/restaurants')
def restaurants():
    restaurants = Restaurants.get_all()
    return render_template('restaurant.html', title="WU Restaurants", avail_rests = restaurants)

@bp.route('/restaurants/filter/<int:attribute>/<int:ordering>', methods=['GET'])
def restaurants_filter(attribute, ordering):
    restaurants = Restaurants.get_all(attribute, ordering)
    return render_template('restaurant.html', title="WU Restaurants", avail_rests = restaurants)

# Fetch and generate a webpage for a specific restaurant
@bp.route('/restaurants/view/<int:rid>', methods=['GET'])
def restaurants_view(rid):
    current_time = datetime.now()
    restaurant = Restaurants.get(rid)
    res_photos = RestaurantPhotos.get(rid)
    is_open = Restaurants.get_if_open(rid, current_time)
    menu = Fooditem.get_menu_for_restaurant(rid)
    reviews = Review.get_all_for_restaurant(rid)
    return render_template('restaurant_view.html', res=restaurant, res_photos=res_photos, now_open = is_open, menu=menu, rev = reviews)

# Fetch a photo from files to display
@bp.route('/restaurants/photos/<filename>')
def get_photo(filename):
    photo_directory = '/home/ubuntu/cs-316-fall-2023-open-project/restaurant_images/'
    try:
        return send_from_directory(photo_directory, filename)
    except Exception as e:
        print(e)
        return None

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

