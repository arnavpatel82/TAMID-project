# this page initialises the website and the necessary frameworks
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secretkey"  
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post

    create_database(app)

    login_manager = LoginManager()
    # if you are not logged in, you will be relocated to the login page
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # lets you access user info given user id of this session's logged in user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
     
    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Database created")