import os

class Config(object):
    # SECRET_KEY = os.environ.get(SECRET_KEY) or "secret_string_bla-bla-bla"
    SECRET_KEY = "secret_string_bla-bla-bla"

    # configure DB connection
    # MONGODB_SETTINGS = {'db': 'UTA_Enrollment', 'host': "mongodb://localhost:27017/UTA_Enrollment"}
    MONGODB_SETTINGS = {'db': 'UTA_Enrollment'}