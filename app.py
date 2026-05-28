from flask import Flask, jsonify, request
from extensions import db, migrate
from models import Clan, Trener, Trening
from flask_cors import CORS
from sqlalchemy import or_

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/teretana'

db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def index():
    return "Početna stranica"

@app.route('/clanovi', methods=['GET'])
def clanovi():
    q = request.args.get('q', '', type=str)
    upit = Clan.query

    if q:
        pojam = f"%{q}%"
        upit = upit.filter(or_(
            Clan.ime.ilike(pojam),
            Clan.prezime.ilike(pojam),
            Clan.email.ilike(pojam),
            Clan.mobitel.ilike(pojam),
            Clan.datum_uclanjenja.ilike(pojam),
        ))

    clanovi = upit.all()

    return [clan.to_dict() for clan in clanovi]

@app.route('/clanovi/<id>', methods=['GET'])
def clan(id):
    clan = Clan.query.filter_by(id=id).first()
    return clan.to_dict()

@app.route('/clanovi', methods=['POST'])
def novi_clan():
    data = request.get_json()

    clan = Clan(
        ime=data.get('ime'),
        prezime=data.get('prezime'),
        email=data.get('email'),
        mobitel=data.get('mobitel'),
        datum_uclanjenja=data.get('datum_uclanjenja')
    )

    db.session.add(clan)
    db.session.commit()

    return "Dodano"

@app.route('/clanovi/<id>', methods=['DELETE'])
def obrisi_clan(id):
    clan = Clan.query.filter_by(id=id).first()

    if not clan:
        return {"error": "Clan not found"}, 404

    db.session.delete(clan)
    db.session.commit()

    return "Obrisano"

@app.route('/clanovi/<id>', methods=['PUT'])
def uredi_clan(id):
    clan = Clan.query.filter_by(id=id).first()
    data = request.get_json()

    clan.ime = data.get('ime')
    clan.prezime = data.get('prezime')
    clan.email = data.get('email')
    clan.mobitel = data.get('mobitel')
    clan.datum_uclanjenja = data.get('datum_uclanjenja')

    db.session.commit()

    return "Ažurirano"

@app.route('/clanovi-dropdown', methods=['GET'])
def clanovi_dropdown():
    clanovi = Clan.query.all()

    return [{
        "title": clan.ime + ' ' + clan.prezime,
        "value": clan.id
    } for clan in clanovi]

@app.route('/treneri', methods=['GET'])
def treneri():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    q = request.args.get('q', '', type=str)

    upit = Trener.query

    if q:
        pojam = f"%{q}%"
        upit = upit.filter(or_(
            Trener.ime.ilike(pojam),
            Trener.prezime.ilike(pojam),
            Trener.specijalizacija.ilike(pojam),
            Trener.email.ilike(pojam)
        ))

    upit = upit.order_by(Trener.id)
    paginacija = upit.paginate(page=page, per_page=per_page, error_out=False)

    if page > paginacija.pages and paginacija.pages > 0:
        paginacija = upit.paginate(page=paginacija.pages, per_page=per_page, error_out=False)

    return jsonify({
        "items": [t.to_dict() for t in paginacija.items],
        "page": paginacija.page,
        "per_page": paginacija.per_page,
        "total": paginacija.total,
        "pages": paginacija.pages
    })

@app.route('/treneri/<id>', methods=['GET'])
def trener(id):
    trener = Trener.query.filter_by(id=id).first()

    if not trener:
        return {"error": "Trener not found"}, 404

    return trener.to_dict()

@app.route('/treneri-dropdown', methods=['GET'])
def treneri_dropdown():
    treneri = Trener.query.all()

    return [{
        "title": t.ime + " " + t.prezime,
        "value": t.id
    } for t in treneri]

@app.route('/treneri', methods=['POST'])
def novi_trener():
    data = request.get_json()

    trener = Trener(
        ime=data.get('ime'),
        prezime=data.get('prezime'),
        specijalizacija=data.get('specijalizacija'),
        email=data.get('email'),
    )

    db.session.add(trener)
    db.session.commit()

    return "Uspješno dodano"

@app.route('/treneri/<id>', methods=['PUT'])
def uredi_trener(id):
    trener = Trener.query.filter_by(id=id).first()

    if not trener:
        return {"error": "Trener not found"}, 404

    data = request.get_json()

    trener.ime = data.get('ime')
    trener.prezime = data.get('prezime')
    trener.specijalizacija = data.get('specijalizacija')
    trener.email = data.get('email')

    db.session.commit()

    return "Ažurirano"

@app.route('/treneri/<id>', methods=['DELETE'])
def obrisi_trener(id):
    trener = Trener.query.filter_by(id=id).first()

    if not trener:
        return {"error": "Trener not found"}, 404

    db.session.delete(trener)
    db.session.commit()

    return "Obrisano"

@app.route('/treninzi', methods=['GET'])
def treninzi():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    q = request.args.get('q', '', type=str)

    upit = Trening.query \
        .outerjoin(Clan, Trening.clan_id == Clan.id) \
        .outerjoin(Trener, Trening.trener_id == Trener.id)

    if q:
        pojam = f"%{q}%"
        upit = upit.filter(or_(
            Clan.ime.ilike(pojam),
            Clan.prezime.ilike(pojam),
            Trener.ime.ilike(pojam),
            Trener.prezime.ilike(pojam),
            Trening.tip.ilike(pojam)
        ))

    upit = upit.order_by(Trening.id)
    paginacija = upit.paginate(page=page, per_page=per_page, error_out=False)

    if page > paginacija.pages and paginacija.pages > 0:
        paginacija = upit.paginate(page=paginacija.pages, per_page=per_page, error_out=False)

    return jsonify({
        "items": [t.to_dict() for t in paginacija.items],
        "page": paginacija.page,
        "per_page": paginacija.per_page,
        "total": paginacija.total,
        "pages": paginacija.pages
    })

@app.route('/treninzi', methods=['POST'])
def dodaj_trening():
    data = request.get_json()

    novi = Trening(
        clan_id=data.get('clan_id'),
        trener_id=data.get('trener_id'),
        opis=data.get('opis'),
        datum=data.get('datum'),
    )

    db.session.add(novi)
    db.session.commit()

    return {"poruka": "Trening dodan"}

if __name__ == "__main__":
    app.run(debug=True)