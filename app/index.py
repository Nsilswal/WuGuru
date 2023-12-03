from flask import render_template
from flask_login import current_user
import datetime

from .models.recommendation import Recommendation
from .models.user import User
from .models.review import Review

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # find the recs current user has published:
    if current_user.is_authenticated:
        reccs = Recommendation.get_all_by_uid_since(current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        revs = Review.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        reccs = None
        revs = None
        return render_template('index.html')
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           Recommendation_history=reccs,
                           Review_history=revs,
                           current_user = current_user
                )
                        
class EditForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Edit')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')
