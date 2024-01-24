from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_required
from flask_sock import Sock

db = SQLAlchemy()
simple_websocket = Sock();

DB_NAME = "pigeons.db"
HOME = "views.home"
ORDERS = "views.orders"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECRET_KEY'] = "pxlsecadv"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    simple_websocket.init_app(app)

    from .auth import auth
    from .views import views
    from .api import api

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(api, url_prefix="/")

    from .models import User, Order, Pigeon

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(app):
    from .models import User, Pigeon, Order
    if not path.exists("instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
            db.session.add(User(
                "Maarten",
                "maarten@sourbron.be",
                "ImUnderYourBed",
                30
            ))
            db.session.add(User(
                "SuperAdmin",
                "pxl@pxl.be",
                "UFhMLVNlY3tUaGVQcm9taXNlZExBTn0=",
                0
            ))
            db.session.add(Pigeon(
                'Sir Coos-a-Lot',
                5,
                5,
                "Had to be muzzled"
            ))
            db.session.add(Pigeon(
                'Feathery McFly',
                1,
                15,
                "Faster than time"
            ))
            db.session.add(Pigeon(
                'Pigeonardo da Vinci',
                14,
                60,
                "Creative problem solving"
            ))
            db.session.add(Pigeon(
                'Beakman Turner Overdrive',
                22,
                8,
                "Saved lives during the war"
            ))
            db.session.add(Pigeon(
                'Wingston Churchill',
                8,
                900,
                "He's hiding something..."
            ))
            db.session.commit()
        print("Created database")
    else:
        print('database already exists')