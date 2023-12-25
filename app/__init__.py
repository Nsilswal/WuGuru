from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .recommendations import bp as rec_bp
    app.register_blueprint(rec_bp)

    from .fooditems import bp as fi_bp
    app.register_blueprint(fi_bp)

    from .reviews import bp as review_bp
    app.register_blueprint(review_bp)

    from .crosscomparisons import bp as crossComp_bp
    app.register_blueprint(crossComp_bp)
    
    from .restaurants import bp as rest_bp
    app.register_blueprint(rest_bp)
    return app
