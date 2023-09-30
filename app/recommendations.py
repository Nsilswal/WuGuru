from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template
from flask import Flask, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
 
from .models.recommendation import Recommendation

bp = Blueprint('recommendations', __name__)

@bp.route('/recommendations')
def recommendations():
    recommendations = Recommendation.get_all()
    # return jsonify([item.__dict__ for item in recommendations])
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
            if Recommendation.register(user_id, form.title.data, form.description.data, formatted_time, init_pop):
                return redirect(url_for('recommendations.recommendations'))
    return render_template('recommendation_add.html', title='Add A Recommendation', form=form)

@bp.route('/recommendations/view/<int:rec_id>', methods=['GET'])
def recommendations_view(rec_id):
    return render_template('recommendation_view.html', title="View Recommendation", rec=Recommendation.get(rec_id))

class RecommendationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Register')