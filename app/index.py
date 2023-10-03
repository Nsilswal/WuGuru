from flask import render_template
from flask_login import current_user
import datetime

from .models.recommendation import Recommendation
from .models.purchase import Purchases

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all user pruchases:
    all_recs = Purchases.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    # find the recs current user has published:
    if current_user.is_authenticated:
        reccs = Recommendation.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        reccs = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           all_reccomendations=all_recs,
                           Recommendation_history=reccs)
