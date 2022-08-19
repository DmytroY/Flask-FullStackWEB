# 'app' is instance of Flask we initiated in __init__.py file
from application import app, db

from flask import render_template, request, json, Response
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

# global variable to be be used in the routines below
courseData = [
    {"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"},
    {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"},
    {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"},
    {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"},
    {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]

@app.route("/")
@app.route("/index")
def index():
    # let's send index=True to the template where implement logic based on it
    return render_template("index.html", index=True)


#API
@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)] # url variables are alvays string type, casting to int is required
    
    return Response(json.dumps(jdata), mimetype="application/json")





@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form, login=True)





@app.route("/register")
def register():
    return render_template("register.html", register=True)


@app.route("/courses/")
@app.route("/courses/<term>") # url variable came to us to be processed later
def courses(term="2019"): # term="2019" by default

    return render_template("courses.html", courseData=courseData, courses=True, term=term)


@app.route("/enrollment", methods=['GET', 'POST'])
# by initial plan this procedure initiated by courses.thml form
def enrollment():
    # reading form imputs, in case of method POST
    if request.method =='POST':
        id = request.form.get('courseID')
        title = request.form.get('title')
        term = request.form.get('term')
    else:
        # reading form imputs, in case of method GET
        id = request.args.get('courseID')
        title = request.args.get('title')
        term = request.args.get('term')

    # render templat in response
    return render_template("enrollment.html", enrollment=True, data={"id":id, "title":title, "term":term })


@app.route("/user")
def user():
    # User(user_id=1, first_name="Chritian", last_name="Hur", email="chris@uta.com", password="abc123").save()
    # User(user_id=2, first_name="Mary", last_name="Jane", email="m.jane@uta.com", password="abc123").save()
    users = User.objects.all()
    #print(users)
    return render_template("user.html", users=users)
    #return("ok")