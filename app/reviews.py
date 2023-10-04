from flask_login import current_user
from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask import Flask, Blueprint
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime
from humanize import naturaldate

from .models.review import Review

bp = Blueprint('reviews', __name__)

@bp.route('/reviews')
def reviews():
    reviews = Review.get_all()
    return render_template('review_home.html', title = "Review Home", avail_reviews = reviews, humanize_time=humanize_time
)

@bp.route('/reviews/filter/<int:attribute>/<int:ordering>', methods=['GET'])
def reviews_filter(attribute, ordering):
    reviews = Review.get_all(attribute, ordering)
    return render_template('review_home.html', title="Review Home", avail_reviews = reviews, humanize_time=humanize_time)

def humanize_time(dt):
    return naturaldate(datetime.date(dt.year, dt.month, dt.day))

