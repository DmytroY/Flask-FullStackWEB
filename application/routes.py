# 'app' is instance of Flask we initiated in __init__.py file
from application import app, db, api

from flask import render_template, request, json, jsonify, Response, redirect, flash, url_for, session
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from flask_restx import Resource

######### API ###################

@api.route('/api', '/api/')
class GetAndPost(Resource):

    # GET all users
    def get(self):
        return jsonify(User.objects.all())

    #POST a user
    def post(self):
        data = api.payload
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        password = data['password']
        user_id = User.objects.count() + 1

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password_hash(password)
        user.save()

        response = jsonify(User.objects(user_id=user_id))
        response.status_code = 201
        return response


@api.route('/api/<idx>')
class GetUpdateDelete(Resource):

    # GET one user
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    # PUT
    def put(self, idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))

    # DELETE
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify(message='record deleted')

######### END API ###################

@app.route("/")
@app.route("/index")
def index():
    # let's send index=True to the template it will help us to highlite 'Home' tab
    return render_template("index.html", index=True)





@app.route("/login", methods=['GET', 'POST'])
def login():
    # check session, may be user already logined
    if session.get('username'):
        return redirect(url_for('index'))

    # using LoginForm class created in 'forms.py" which inherits FlaskForm
    form = LoginForm()
    if form.validate_on_submit() == True:
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.user_id
            session['username'] =user.first_name
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry, something went wrong", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    # check session, may be user already logined
    if session.get('username'):
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit() == True:
        email = form.email.data
        password = form.password.data
        first_name = form.fist_name.data
        last_name = form.last_name.data

        user_id = User.objects.count() +1
        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password_hash(password)
        user.save()
        flash(f"{first_name}, you are successfully registered!", "success")
        return redirect(url_for("index"))

    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/courses/")
@app.route("/courses/<term>") # url variable came to us to be processed later
def courses(term="2019"):

    courseData = Course.objects.order_by("-courseID") # extract all Course records and order by decending courseID
    return render_template("courses.html", courseData=courseData, courses=True, term=term)


@app.route("/enrollment", methods=['GET', 'POST'])



# by initial plan this procedure initiated by courses.thml form
def enrollment():

    #check if user logoned
    if not session.get('username'):
        return redirect(url_for('login'))

    # reading form imputs, method is POST
    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Sorry, you already registered for the course {courseTitle}","danger")
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}", "success")

    classes = list( User.objects.aggregate(*[
                {
                    '$lookup': {
                        'from': 'enrollment', 
                        'localField': 'user_id', 
                        'foreignField': 'user_id', 
                        'as': 'r1'
                    }
                }, {
                    '$unwind': {
                        'path': '$r1', 
                        'includeArrayIndex': 'r1_id', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$lookup': {
                        'from': 'course', 
                        'localField': 'r1.courseID', 
                        'foreignField': 'courseID', 
                        'as': 'r2'
                    }
                }, {
                    '$unwind': {
                        'path': '$r2', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$match': {
                        'user_id': user_id
                    }
                }, {
                    '$sort': {
                        'couseID': -1
                    }
                }
            ]))

    return render_template("enrollment.html", enrollment=True, title="Enrolment", classes=classes)


@app.route("/user")
def user():
    users = User.objects.all()
    return render_template("user.html", users=users)
