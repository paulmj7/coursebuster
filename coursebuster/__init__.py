from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coursebuster.db'
app.config['SECRET_KEY'] = '04942fc1356fe0cafff1264614f918f1'


db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from coursebuster import routes
