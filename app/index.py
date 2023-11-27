from flask import jsonify, redirect, url_for, flash, render_template, request, send_from_directory
from flask_login import current_user
import datetime
from humanize import naturaldate

from .models.recommendation import Recommendation
from .models.purchase import Purchase
from .models.review import Review


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

@bp.route('/delete', methods=['POST'])
def review_delete():
    review = request.form['review_id']
    Review.delete(int(review))
    return redirect(url_for('index.index'))

def humanize_time(dt):
    return naturaldate(datetime.date(dt.year, dt.month, dt.day))
