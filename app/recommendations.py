from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
 
from .models.recommendation import Recommendation
from .models.rec_photo import Rec_Photo

bp = Blueprint('recommendations', __name__)

@bp.route('/recommendations')
def recommendations():
    recommendations = Recommendation.get_all()
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations)

@bp.route('/recommendations/filter', methods=['POST'])
def recommendations_filter():
    attr = request.form['Attribute']
    order = request.form['Ordering']
    recommendations = Recommendation.get_all(attr, order)
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations)

@bp.route('/recommendations/search', methods=['GET'])
def recommendations_search():
    keyword = request.args.get('query')
    recommendations = Recommendation.search_by_title(keyword)
    return render_template('recommendation_home.html', title="Recommendation Home", avail_recs = recommendations)

@bp.route('/recommendations/add', methods=['POST'])
def recommendation_add():
    form = RecommendationForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user_id = current_user.id
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
            init_pop = 0
            rec_id = Recommendation.register(user_id, form.title.data, form.description.data, formatted_time, init_pop).id
            if rec_id:
                Rec_Photo.register(rec_id, form.photo.data)
                return redirect(url_for('recommendations.recommendations'))
    return render_template('recommendation_add.html', title='Add A Recommendation', form=form)

@bp.route('/recommendations/view/<int:rec_id>', methods=['GET'])
def recommendations_view(rec_id):
    rec_photos = Rec_Photo.get_all(rec_id)
    return render_template('recommendation_view.html', title="View Recommendation", rec=Recommendation.get(rec_id), photos=rec_photos)

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
    submit = SubmitField('Register') 

