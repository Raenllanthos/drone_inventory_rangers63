from flask import Blueprint, render_template, request, redirect, url_for, flash
from drone_inventory.models import User,db, check_password_hash
from drone_inventory.forms import UserLoginForm

# Imports for flask login
from flask_login import login_user, logout_user, current_user, login_required

"""
    Some arguments are specified when creating the Blueprint object.
    The first argument "site", is the blueprint name,
    which is used by Flask's routing mechanism.

    The second argument, __name__, is the Blueprint's import name,
    this is how flask locates the blueprint's resources.
"""

auth = Blueprint("auth", __name__, template_folder="auth_templates")

@auth.route("/signup", methods = ['GET', 'POST'])
# get gets data from our database, post means they can post on page; methods work universally
# GET/POST/PUT/DELETE are HTTP verbs that describe what we want to do at a given endpoint (location)
def signup():
    form = UserLoginForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a user account, {email}", "user-created")

            return redirect(url_for('site.index'))
    except:
        raise Exception("Invalid Form Data: Please Check your form")
    return render_template("signup.html", form=form)

@auth.route("/signin", methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("You were successfullt loggin in: via Email/Password", "auth-success")
                return redirect(url_for("site.profile"))
            else:
                flash("Your Email/Password is incorrect! Try Again!", "auth-failed")
                return redirect(url_for("auth.signin"))
    except:
        raise Exception("Invalid Form Data: Please Check Your Form!")
    return render_template("signin.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("site.index"))