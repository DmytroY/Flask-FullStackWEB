from flask import Flask

# instantiate Flask
app = Flask(__name__)

# we can describe routes and assosiated procedures here,
# but we prefer do it in separate file 'routes'
from application import routes