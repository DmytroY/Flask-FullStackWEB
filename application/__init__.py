from flask import Flask
from .config import Config # import configuration class with address of connection to DB and secret key
from flask_mongoengine import MongoEngine

# instantiate Flask
app = Flask(__name__)

# take configuration options from Config class
app.config.from_object(Config) 

# instantiate and initilaze DB engine
db = MongoEngine()
db.init_app(app)

# we can describe routes and assosiated procedures right here,
# but we prefer do it in separate file 'routes'
from application import routes