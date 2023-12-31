# Recommendations contains all of the endpoints relevant to viewing and changing recommendations.

import random

from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import current_app as app
from flask import Blueprint
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectMultipleField
from wtforms.validators import DataRequired
from datetime import datetime
 
from .models.recommendation import Recommendation
from .models.rec_photo import Rec_Photo
from .models.rec_tag import Rec_Tag
from .models.rec_food import Rec_Food
from .models.user import User
from .models.fooditem import Fooditem

bp = Blueprint('recommendations', __name__)

# Default route - displays all recommendations, ranked by popularity
@bp.route('/recommendations')
def recommendations():
    recommendations = Recommendation.get_all()
    is_logged_in = current_user.is_authenticated
    highlight_message = generate_highlight_message()
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in, banner_message = highlight_message)

# Returns a list of recommendations based on an attribute and ordering
@bp.route('/recommendations/filter', methods=['POST'])
def recommendations_filter():
    attr = request.form['Attribute']
    order = request.form['Ordering']
    recommendations = Recommendation.get_all(attr, order)
    is_logged_in = current_user.is_authenticated
    highlight_message = generate_highlight_message()
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in, banner_message = highlight_message)

# Returns a list of recommendations based on keyword matches
@bp.route('/recommendations/search', methods=['GET'])
def recommendations_search():
    keyword = request.args.get('query')
    recommendations = Recommendation.search_by_keyword(keyword)
    is_logged_in = current_user.is_authenticated
    highlight_message = generate_highlight_message()
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in, banner_message = highlight_message)

# Returns a list of recommendations based on tag matches
@bp.route('/recommendations/tagsearch/<tagname>', methods=['GET'])
def recommendations_tag_search(tagname):
    recommendations = Recommendation.get_all_for_tag(tagname)
    is_logged_in = current_user.is_authenticated
    highlight_message = generate_highlight_message()
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in, banner_message = highlight_message)

# Returns a list of recommendations made by the current user (if logged in)
@bp.route('/recommendation/filter/mine', methods=['GET'])
def recommendations_get_mine():
    if current_user.is_authenticated:
        recommendations = Recommendation.get_all_by_uid_since(current_user.id, datetime(1980, 9, 14, 0, 0, 0))
        is_logged_in = current_user.is_authenticated
        return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in)
    return recommendations()

# Add a recommendation    
@bp.route('/recommendations/add', methods=['POST'])
def recommendation_add():
    form = RecommendationForm()
    form.related_foods.choices = Fooditem.generate_full_pairings()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user_id = current_user.id
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
            init_pop = 0
            rec_id = Recommendation.register(user_id, form.title.data, form.description.data, formatted_time, init_pop).id
            if rec_id:
                Rec_Photo.register(rec_id, form.photo.data)
                Rec_Tag.register(rec_id, form.related_tags.data)
                Rec_Food.register(rec_id, form.related_foods.data)
                return redirect(url_for('recommendations.recommendations'))
    return render_template('recommendation_add.html', title='Add A Recommendation', form=form)

# Update a recommendation based on the new submitted values
@bp.route('/recommendations/edit/<int:rec_id>', methods=['POST'])
def recommendations_edit(rec_id):
    target_rec = Recommendation.get(rec_id)
    current_title = target_rec.title
    current_description = target_rec.description
    # Create an instance of the form and set dynamic values
    form = RecommendationForm(
        title=current_title,
        description=current_description
    )
    form.related_foods.choices = Fooditem.generate_full_pairings()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
            success = Recommendation.update(rec_id, form.title.data, form.description.data, formatted_time)
            if success:
                Rec_Photo.register(rec_id, form.photo.data)
                Rec_Tag.register(rec_id, form.related_tags.data)
                Rec_Food.register(rec_id, form.related_foods.data)
                return recommendations_view(rec_id)
    return render_template('recommendation_add.html', title='Edit This Recommendation', form=form)

# Delete a recommendation
@bp.route('/recommendations/delete/<int:rec_id>', methods=['POST'])
def recommendations_delete(rec_id):
    target_rec = Recommendation.get(rec_id)
    if not current_user.is_authenticated or current_user.id != target_rec.user_id:
        return recommendations_view(rec_id)
    success = Recommendation.delete(rec_id)
    return recommendations()

# Fetch and generate a webpage for a specific recommendation
@bp.route('/recommendations/view/<int:rec_id>', methods=['GET'])
def recommendations_view(rec_id):
    rec_info = Recommendation.get(rec_id)
    rec_photos = Rec_Photo.get_all(rec_id)
    rec_tags = Rec_Tag.get_all_for_entry(rec_id)
    user_creator = User.get(rec_info.user_id)
    nutrition_summary = Rec_Food.generate_summary_for_rec(rec_id)
    is_owner = current_user.is_authenticated and current_user.id == user_creator.id
    return render_template('recommendation_view.html', title="View Recommendation", rec=rec_info, photos=rec_photos, user=user_creator, tags=rec_tags, nutrition_summary=nutrition_summary, display_edit=is_owner, is_logged_in=current_user.is_authenticated)

# Upvote (increase popularity) of a recommendation
@bp.route('/recommendations/upvote/<int:rec_id>', methods=['POST'])
def recommendations_upvote(rec_id):
    Recommendation.change_popularity(rec_id, 1)
    return recommendations_view(rec_id)

# Fetch a photo from files to display
@bp.route('/recommendations/photos/<filename>')
def get_photo(filename):
    photo_directory = '/home/ubuntu/cs-316-fall-2023-open-project/photos'
    try:
        return send_from_directory(photo_directory, filename)
    except Exception as e:
        print(e)
        return None

# FlaskForm format to collect data to add new/update existing recommendations
class RecommendationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    photo = FileField('Photo Upload')
    related_tags = SelectMultipleField('Select Meal Tags', choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack')
        ])
    related_foods = SelectMultipleField('Select Related Foods')
    submit = SubmitField('Register') 

# Generate a random awards message at the top of the home page, based off rankings of a food's appearance and total popularity
def generate_highlight_message():
    top_appearing_foods = Rec_Food.get_most_attached()
    top_popular_foods = Rec_Food.get_most_popular()
    rand_appearing_rank = random.randint(0, 9)
    rand_pop_rank = random.randint(0, 9)
    selected_appearing_food = top_appearing_foods[rand_appearing_rank]
    selected_pop_food = top_popular_foods[rand_pop_rank]
    message = f'TRENDING NOW: Currently, {selected_appearing_food[0]} from {selected_appearing_food[1]} is #{rand_appearing_rank + 1} in total mentions! Additionally, check out this rising contender: {selected_pop_food[0]} from {selected_pop_food[1]} is #{rand_pop_rank + 1} in total popularity - yum!'
    return message