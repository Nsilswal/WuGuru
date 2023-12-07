from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
import datetime
from humanize import naturaldate
import statistics

from .models.review import Review
from .models.user import User
from .models.restaurant import Restaurants

bp = Blueprint('reviews', __name__)

@bp.route('/reviews')
# home page for reviews, shows all reviews in database sorted by date descending
def reviews():
    reviews = Review.get_all()
    restaurants = Restaurants.get_all()
    average = 0
    if len(reviews) > 0:
        average = statistics.mean([float(review.rating) for review in reviews])
    return render_template('review_home.html', title = "Review Home", avail_reviews = reviews, avail_rests = restaurants, humanize_time=humanize_time, avg = f'{average:.2f}')

@bp.route('/reviews/filter', methods=['POST'])
# shows reviews filtered by restaurant and/or sorted by date or rating
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
    average = 0
    if len(reviews) > 0:
        average = statistics.mean([float(review.rating) for review in reviews])
    return render_template('review_home.html', title="Review Home", avail_reviews = reviews, avail_rests = restaurants, humanize_time=humanize_time, avg = f'{average:.2f}')

@bp.route('/reviews/add', methods=['POST'])
# goes to create new review form page, if data inputted in form is valid, creates new review and redirects to review home page
def review_add():
    form = ReviewForm()
    form.restaurant.choices = [(restaurant.id, restaurant.name) for restaurant in Restaurants.get_all()]
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user_id = current_user.id 
            Review.create(user_id, datetime.date.today(), int(form.rating.data), form.description.data, int(form.restaurant.data), form.anonymous.data)
            return redirect(url_for('reviews.reviews'))
    return render_template('review_add.html', title='Add A Review', form=form)

@bp.route('/reviews/update/<int:id>', methods=['GET', 'POST'])
# goes to update existing review form page, if data inputted in form is valid, updates review and redirects to user home page
def review_update(id):
    if current_user.is_authenticated:
        review = Review.get(id) 
        if review and current_user.id == review.user_id:
            restaurant_id = review.restaurant_id
            form = ReviewForm(rating=review.rating, restaurant=restaurant_id, description=review.description, anonymous=review.anonymous)
            form.restaurant.choices = [(restaurant.id, restaurant.name) for restaurant in Restaurants.get_all()]
            if request.method == "POST" and form.validate_on_submit():
                Review.update(id, datetime.date.today(), int(form.rating.data), form.description.data, int(form.restaurant.data), form.anonymous.data)
                return redirect(url_for('index.index'))
            else:
                return render_template('review_update.html', title='Update Review', form=form, review=review)
        else:
            return "Sorry, you cannot access this page or this page does not exist."
    else:
        return "Sorry, you cannot access this page or this page does not exist."

@bp.route('/reviews/delete', methods=['POST'])
# deletes review and redirects to user home page
def review_delete():
    review_id = request.form['review_id']
    if current_user.is_authenticated:
        Review.delete(int(review_id))
    return redirect(url_for('index.index'))

@bp.route('/reviews/search', methods=['GET'])
# shows all reviews with descriptions containing keyword
def reviews_search():
    keyword = request.args.get('query')
    reviews = Review.search_by_keyword(keyword)
    restaurants = Restaurants.get_all()
    average = 0
    if len(reviews) > 0:
        average = statistics.mean([float(review.rating) for review in reviews])
    return render_template('review_home.html', title="Review Home", avail_reviews = reviews, avail_rests = restaurants, humanize_time=humanize_time, avg = f'{average:.2f}')

def humanize_time(dt):
    return naturaldate(datetime.date(dt.year, dt.month, dt.day))

class ReviewForm(FlaskForm):
    restaurant = SelectField('Select restaurant', choices = [], validators=[DataRequired()])
    rating = SelectField('Select rating', choices=[1, 2, 3, 4, 5], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=300)])
    anonymous = BooleanField('Leave review anonymously?')
    submit = SubmitField('Submit')

