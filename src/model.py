from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

app.config.from_pyfile("../config.py")

mail = Mail(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from .classes import user, categorie, souscategorie, motcles, annonce, image, favoris, localite, vendu, image



with app.app_context():
    db.create_all()

def save(entity):
    db.session.add(entity)
    db.session.commit()
