from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from .models import User
from . import HOME

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=username).first()
        if user:
            if password == user.password:
                flash("Logged in!", category="info")
                login_user(user, remember=True)
                return redirect(url_for(HOME))
            else:
                flash("Incorrect login", category="error")
        else:
            flash("Incorrect login", category="error")
        
    
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out!", category="info")
    return redirect(url_for(HOME))

