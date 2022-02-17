from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin


db = SQLAlchemy()
admin = Admin()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    admin.init_app(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    from blueprints.open import bp_open
    app.register_blueprint(bp_open)

    from blueprints.user import bp_user
    app.register_blueprint(bp_user)

    from blueprints.admin import bp_admin
    app.register_blueprint(bp_admin)

    from blueprints.api import bp_api
    app.register_blueprint(bp_api, url_prefix='/api/v1.0')

    return app


app = create_app()
migrate = Migrate(app, db)
