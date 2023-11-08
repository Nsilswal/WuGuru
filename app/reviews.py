from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
import datetime
from humanize import naturaldate

from .models.review import Review
from .models.user import User
from.models.restaurant import Restaurants

bp = Blueprint('reviews', __name__)

@bp.route('/reviews')
def reviews():
    reviews = Review.get_all()
    restaurants = Restaurants.get_all()
    return render_template('review_home.html', title = "Review Home", avail_reviews = reviews, avail_rests = restaurants, humanize_time=humanize_time
)

@bp.route('/reviews/filter', methods=['POST'])
def reviews_filter():
    attribute = request.form['Attribute']
    ordering = request.form['Ordering']
    restaurant_id = request.form['Restaurant']
    reviews = []
    if restaurant_id == 'None':
        reviews = Review.get_all(attribute, ordering)
    else:
        reviews = Review.get_all_for_restaurant(int(restaurant_id), attribute, ordering)
    restaurants = Restaurants.get_all()
    return render_template('review_home.html', title="Review Home", avail_reviews = reviews, avail_rests = restaurants, humanize_time=humanize_time)

@bp.route('/reviews/add', methods=['POST'])
def review_add():
    form = ReviewForm()
    form.restaurant.choices = [(restaurant.id, restaurant.name) for restaurant in Restaurants.get_all()]
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user_id = current_user.id 
            rev_id = Review.create(user_id, datetime.date.today(), int(form.rating.data), form.description.data, int(form.restaurant.data))
            if rev_id:
                return redirect(url_for('reviews.reviews'))
    return render_template('review_add.html', title='Add A Review', form=form)

def humanize_time(dt):
    return naturaldate(datetime.date(dt.year, dt.month, dt.day))

class ReviewForm(FlaskForm):
    restaurant = SelectField('Select restaurant', choices = [], validators=[DataRequired()])
    rating = SelectField('Select rating', choices=[1, 2, 3, 4, 5], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    submit = SubmitField('Submit')

