from re import L
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.food import Food
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/logreg")
def logreg():
    return render_template("logOrReg.html")

@app.route("/register", methods = ["POST"])
def register():
    if not User.validate_reg(request.form):
        return redirect("/logreg")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    data = {
        'username' : request.form['username'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect ('/dashboard')

@app.route("/login", methods = ["POST"])
def login():
    data = {'email' : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect('/logreg')
    if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/logreg')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route("/dashboard")
def dashoard():
    if "user_id" not in session:
        return redirect('/logout')
    data = {
        'id' : session["user_id"]
    }
    print(session)
    return render_template('dashboard.html', user = User.get_by_id(data), foods = Food.get_all())

@app.route("/myprofile/<int:id>")
def profile(id):
    if "user_id" not in session:
        return redirect('/logout')
    data = {
        'id' : session["user_id"]
    }
    print(session)
    return render_template('profile_page.html', user = User.get_by_id(data), foods = Food.get_all())

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')