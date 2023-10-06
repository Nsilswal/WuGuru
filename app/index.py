from flask import render_template
from flask_login import current_user
import datetime

from .models.recommendation import Recommendation
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all user pruchases:
    # find the recs current user has published:
    if current_user.is_authenticated:
        reccs = Recommendation.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        all_purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        reccs = None
        all_purchases = None
        return render_template('index.html')
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           all_purch=all_purchases,
                           Recommendation_history=reccs)
