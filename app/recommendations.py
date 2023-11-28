from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import current_app as app
from flask import Flask, Blueprint
import os
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
 
from .models.recommendation import Recommendation
from .models.rec_photo import Rec_Photo
from .models.rec_tag import Rec_Tag
from .models.rec_food import Rec_Food
from .models.user import User
from .models.fooditem import Fooditem

bp = Blueprint('recommendations', __name__)

@bp.route('/recommendations')
def recommendations():
    recommendations = Recommendation.get_all()
    is_logged_in = current_user.is_authenticated
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in)

@bp.route('/recommendations/filter', methods=['POST'])
def recommendations_filter():
    attr = request.form['Attribute']
    order = request.form['Ordering']
    recommendations = Recommendation.get_all(attr, order)
    is_logged_in = current_user.is_authenticated
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in)

@bp.route('/recommendations/search', methods=['GET'])
def recommendations_search():
    keyword = request.args.get('query')
    recommendations = Recommendation.search_by_keyword(keyword)
    is_logged_in = current_user.is_authenticated
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in)

@bp.route('/recommendations/tagsearch/<tagname>', methods=['GET'])
def recommendations_tag_search(tagname):
    recommendations = Recommendation.get_all_for_tag(tagname)
    is_logged_in = current_user.is_authenticated
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in)

@bp.route('/recommendation/filter/mine', methods=['GET'])
def recommendations_get_mine():
    if current_user.is_authenticated:
        recommendations = Recommendation.get_all_by_uid_since(current_user.id, datetime(1980, 9, 14, 0, 0, 0))
        is_logged_in = current_user.is_authenticated
        return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations, logged_in=is_logged_in)
    return recommendations()

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

@bp.route('/recommendations/delete/<int:rec_id>', methods=['POST'])
def recommendations_delete(rec_id):
    target_rec = Recommendation.get(rec_id)
    if not current_user.is_authenticated or current_user.id != target_rec.user_id:
        return recommendations_view(rec_id)
    success = Recommendation.delete(rec_id)
    return recommendations()
    
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

@bp.route('/recommendations/view/<int:rec_id>', methods=['GET'])
def recommendations_view(rec_id):
    rec_info = Recommendation.get(rec_id)
    rec_photos = Rec_Photo.get_all(rec_id)
    rec_tags = Rec_Tag.get_all_for_entry(rec_id)
    rec_foods = Rec_Food.get_all_names_for_entry(rec_id)
    user_creator = User.get(rec_info.user_id)
    is_owner = current_user.is_authenticated and current_user.id == user_creator.id
    return render_template('recommendation_view.html', title="View Recommendation", rec=rec_info, photos=rec_photos, user=user_creator, tags=rec_tags, foods=rec_foods, display_edit=is_owner)

@bp.route('/recommendations/upvote/<int:rec_id>', methods=['POST'])
def recommendations_upvote(rec_id):
    Recommendation.change_popularity(rec_id, 1)
    return recommendations_view(rec_id)

@bp.route('/recommendations/photos/<filename>')
def get_photo(filename):
    photo_directory = '/home/ubuntu/cs-316-fall-2023-open-project/photos'
    try:
        return send_from_directory(photo_directory, filename)
    except Exception as e:
        print(e)
        return None

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


