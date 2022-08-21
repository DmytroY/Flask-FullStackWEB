from flask import Flask
from .config import Config # import configuration class with address of connection to DB and secret key
from flask_mongoengine import MongoEngine
from flask_restx import Api


# instantiate of Flask, Api and Mongo
app = Flask(__name__)
api = Api()
db = MongoEngine()

# take configuration options from Config class
app.config.from_object(Config) 

# initialize Api andd DB engines
api.init_app(app)
db.init_app(app)

# we can describe routes and assosiated procedures right here,
# but we prefer do it in separate file 'routes'
from application import routes