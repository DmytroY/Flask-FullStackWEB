# Here everything starts.
# In case of we do not use .flaskenv file
# eitger app.py or application.py will run first,
# but we specified environment variable FLASK_APP=main.py in .flaskenv file,
# so main.py run first


from application import app
# Flask will search in application/__init__.py file and here is 'app' procedure will be run