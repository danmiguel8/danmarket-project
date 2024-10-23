import os
from src .model import app

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '40c0be5e20ac11'
app.config['MAIL_PASSWORD'] = '9488b3703504c1'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

DEBUG = True
APP_NAME = "DanMarket"
# print(f"{APP_NAME}")
CLIENT = "client"

ADMIN = "admin"

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR,"DanMarket.sqlite")

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "HereIsMySecretKey"

NO_IMG = "https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg"