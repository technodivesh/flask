
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)



app.config['SECRET_KEY'] = 'f18967deeee433fb67a0d6f7422067d7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from flaskblog import routes