from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from .models import Pigeon, Order
from . import HOME
from . import db

views = Blueprint("views", __name__)

@views.route("/home")
@views.route("/")
@login_required
def home():
    pigeons = Pigeon.query.all()
    return render_template("index.html", user=current_user, pigeons=pigeons)

@views.route("/orders")
@login_required
def orders():
    orders = db.session.query(Order, Pigeon).filter_by(owner=current_user.id).join(Pigeon).all(); # // Order.query.filter_by(owner=current_user.id).join(Pigeon).all()

    for order, pigeon in orders:
        print(order, pigeon.name)

    return render_template("orders.html", user=current_user, orders=orders)