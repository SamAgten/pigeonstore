import json
from flask import Blueprint, abort, flash, redirect, request, url_for
from flask_login import current_user, login_required
from flask_sock import Sock
from . import db, HOME, ORDERS

from .models import Order, Pigeon

api = Blueprint("api", __name__)

def order(data):
    pigeon = data.form.get("pigeon")
    if pigeon is None:
        abort(400)

    p = Pigeon.query.filter_by(id=pigeon).first()
    if p is None:
        db.session.rollback()
        flash('No such pigeon!', category='error')
        return redirect(url_for(HOME))
    
    current_user.pigeon_coins -= p.price
    if current_user.pigeon_coins < 0:
        db.session.rollback()
        flash('Not enough money for this pigeon!', category='error')
        return redirect(url_for(HOME))
    
    db.session.add(Order(
        pigeon,
        1,
        1
    ))
    db.session.add(current_user)
    db.session.commit()

    flag = "PXL-Sec{RaceToTheTop}"
    if p.id == 5:
        flash(f"My! You have a lot of money, have a complementary flag: {flag}", category="info")
    else:
        flash(f"Pigeon ordered!", category="info")
    
    return redirect(url_for(HOME))

def cancel(data):

    order = data.form.get("order")
    if order is None:
        abort(400)

    o = Order.query.filter_by(id=order).first()
    if o is None:
        db.session.rollback()
        flash('No such order exists!', category='error')
        return redirect(url_for(ORDERS))
    
    p = Pigeon.query.filter_by(id=o.pigeon).first()
    if p is None:
        db.session.rollback()
        flash('Order for an invalid pigeon', category='error')
        return redirect(url_for(ORDERS))
    
    current_user.pigeon_coins += p.price;
    db.session.add(current_user)
    db.session.delete(o)
    db.session.commit()

    
    flash('Order deleted', category='info')
    return redirect(url_for(ORDERS))

request_handlers = {
    "order": order,
    "cancel": cancel
}

@api.route("/api", methods=['POST'])
@login_required
def route():
    
    if request.method != 'POST':
        abort(405)

    req = request.form.get('request')
    if req is None:
        print('here')
        abort(400)

    if req not in request_handlers:
        abort(400)

    return request_handlers[req](request)

