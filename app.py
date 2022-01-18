from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from blueprints.open import bp_open
    app.register_blueprint(bp_open)

    from blueprints.user import bp_user
    app.register_blueprint(bp_user)

    from blueprints.admin import bp_admin
    app.register_blueprint(bp_admin)

    return app
