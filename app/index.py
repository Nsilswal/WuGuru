from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask_login import current_user
import datetime
from humanize import naturaldate

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
                           humanize_time=humanize_time)

def humanize_time(dt):
    return naturaldate(datetime.date(dt.year, dt.month, dt.day))
#create a form that authenticated users can use to edit their account information
class EditForm(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    email = StringField('Email')
    password = PasswordField('Password', validators=[])
    password2 = PasswordField(
        'Repeat Password', validators=[
                                       EqualTo('password')])
    submit = SubmitField('Edit')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/user_edit', methods=['GET', 'POST'])
def Edit():
    form = EditForm()
    if form.validate_on_submit():
        if User.edit(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data, current_user.id):
            flash('Edits have been processed!')
        return redirect(url_for('users.login'))
    return render_template('user_edit.html', title='Edit Account Info', form=form)