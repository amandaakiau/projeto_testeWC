from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def get_connection():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/estacionamento'
    return app
