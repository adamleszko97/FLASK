from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


login = LoginManager()

engine = create_engine("mssql+pymssql://ale:Test12345!@sqlflasktest.database.windows.net/test", echo=True)
db = declarative_base()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdf'

    login.init_app(app)
    login.login_view = 'auth.login'
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")


    return app

    