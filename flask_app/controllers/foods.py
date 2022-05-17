from email.mime import image
import os
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.food import Food
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/food/new")
def new_foods():
    if 'user_id' not in session : 
        return redirect('/logreg')
    data = {
        'id' : session['user_id']
    }
    return render_template("new_food.html", user = User.get_by_id(data))

@app.route("/view/<string:state>")
def view_by_state(state):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'state' : state
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template("view_state.html", foods = Food.get_by_state(data), user = User.get_by_id(user_data), state = state)

@app.route("/view/food/<int:id>")
def view_one_food(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template("view_one_food.html", food = Food.show_one(data), user = User.get_by_id(user_data))


@app.route('/create', methods = ['POST'])
def create_food():
    if 'user_id' not in session:
        return redirect("/logreg")
    if not Food.validate_food(request.form):
        return redirect('/dashboard')
    data = {
        'state' : request.form["state"],
        'city' : request.form["city"],
        'restaraunt' : request.form["restaraunt"],
        'dish' : request.form["dish"],
        "descRev" : request.form["descRev"],
        'rating' : request.form["rating"],
        'user_id' : session['user_id']
    }
    Food.save(data)
    return redirect('/dashboard')

@app.route('/edit/food/<int:id>')
def edit_food(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template("edit_food.html", edit = Food.show_one(data), user = User.get_by_id(user_data))

@app.route("/update/food", methods = ["POST"])
def update_food():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Food.validate_food(request.form):
        return redirect('/dashboard')
    data = {
        'city' : request.form["city"],
        'state' : request.form["state"],
        'restaraunt' : request.form["restaraunt"],
        'dish' : request.form["dish"],
        "descRev" : request.form["descRev"],
        'rating' : request.form["rating"],
        'id' : request.form['id']
    }
    Food.update(data)
    return redirect('/dashboard')

@app.route("/delete/<int:id>")
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    Food.delete(data)
    return redirect('/dashboard')

# @app.route('/view/<string:state>')