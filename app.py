from flask import Flask
from extensions import db, migrate
from models import Clan

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/teretana'

db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def index():
    return "Početna stranica"

@app.route('/clanovi/<ime>/<prezime>/<email>/<mobitel>/<datum_uclanjenja>')
def clanovi(ime, prezime, email, mobitel, datum_uclanjenja):

    clan = Clan(ime=ime, prezime=prezime, email=email, mobitel=mobitel, datum_uclanjenja=datum_uclanjenja)
    db.session.add(clan)
    db.session.commit()

    return "Dodano"

app.run(debug=True)