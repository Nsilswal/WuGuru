from flask_login import current_user
from flask import jsonify
from flask import Flask, Blueprint
 
from .models.recommendation import Recommendation

bp = Blueprint('recommendations', __name__)

@bp.route('/recommendations')
def recommendations():
    recommendations = Recommendation.get_all()
    return jsonify([item.__dict__ for item in recommendations])
