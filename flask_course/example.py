from pathlib import Path
from typing import Dict, List
import json
from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages, session
# local
from flask_course.utils import validate_creation, validate_update
from flask_course.data.storage import DataStorage

p = Path(__file__).parent.joinpath("data/users.json")
data_storage = DataStorage(p)
app = Flask(__name__)
app.secret_key = "secret_key_123123123"


@app.route('/')
def index():
    return 'Hello, World!'


@app.get("/login")
def user_login():
    user = {}
    errors = {}
    return render_template("users/login.html", user=user, errors=errors)

@app.post("/login")
def login():
    data = request.form.to_dict()
    user = data_storage.find_by_email(data["email"])
    if user:
        session["authorized"] = True

        return redirect(url_for("users"), code=302)

    return redirect(url_for("login"), code=402)


@app.route("/logout", methods=["POST", "DELETE"])
def logout():
    session["authorized"] = False

    return redirect(url_for("login"), code=302)


@app.route('/users')
def users():
    if not session.get("authorized", False):
        return redirect(url_for("login"), code=302)

    result = data_storage.get()
    name = request.args.get("nickname")
    messages = get_flashed_messages(with_categories=True)

    if name:
        result = [
            user for user in result if name in user["nickname"]
        ]
    return render_template(
        'users/index.html',
        users = result,
        search = name,
        messages=messages
    )


@app.route("/users/new")
def show_new_user_form():
    errors = {}
    user = {}
    return render_template(
        "users/new.html",
        errors=errors,
        user=user
    )


@app.get("/users/<id>/edit")
def edit_user(id):
    user = data_storage.find(id)
    if user:
        errors = {}
        return render_template(
            "users/edit.html",
            user=user,
            errors=errors
        )

    return "Can't find user", 404


@app.post("/users/<id>/patch")
def patch_user(id):
    user_list = data_storage.get()
    user = data_storage.find(id)

    if user:
        new_user = request.form.to_dict()
        new_user["id"] = user["id"]

        errors = validate_update(
            new_data=new_user,
            users_list=user_list
        )

        if not errors:
            user["nickname"] = new_user["nickname"]
            user["email"] = new_user["email"]
            data_storage.save(user)
            flash("user updated!!!", "success")
            return redirect(url_for("users"), code=302)

        return render_template(
            "users/edit.html",
            user=new_user,
            errors=errors
        )

    return "Can't find user", 404

@app.post("/users")
def create_user():
    new_user = request.form.to_dict()
    users_list = data_storage.get()
    errors = validate_creation(
        new_data=new_user,
        users_list=users_list
    )
    if not errors:
        data_storage.save(new_user)
        flash(
            message=f"user {new_user['nickname']} added!", 
            category="success"
        )
        return redirect(url_for('users'), code=302)

    return render_template(
        "users/new.html",
        errors=errors,
        user=new_user
    ), 422


@app.get("/users/<id>/delete")
def user_delete(id):
    user = data_storage.find(id)
    return render_template(
        "users/delete.html",
        user=user
    )


@app.post("/users/<id>/delete")
def delete_user(id):
    data_storage.delete(id)
    return redirect(url_for("users"), code=302)
