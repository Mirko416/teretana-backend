from extensions import db

class Clan(db.Model):
    __tablename__ = 'clanovi'

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(30), nullable=False)
    prezime = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mobitel = db.Column(db.Integer, nullable=False)
    datum_uclanjenja = db.Column(db.Date, nullable=False)

    pretplate = db.relationship('Pretplata', backref='clan', lazy=True)
    treninzi = db.relationship('Trening', backref='clan', lazy=True)

class Trener(db.Model):
    __tablename__ = 'treneri'

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(30), nullable=False)
    prezime = db.Column(db.String(30), nullable=False)
    specijalizacija = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    treninzi = db.relationship('Trening', backref='trener', lazy=True)
class Clanarina(db.Model):
    __tablename__ = 'clanarine'

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    cijena = db.Column(db.Numeric(10,2), nullable=False)
    duzina_trajanja = db.Column(db.Integer, nullable=False)

    pretplate = db.relationship('Pretplata', backref='clanarine', lazy=True)

class Pretplata(db.Model):
    __tablename__ = 'pretplate'
    id = db.Column(db.Integer, primary_key=True)
    datum_pocetka = db.Column(db.Date, nullable=False)
    datum_zavrsetka = db.Column(db.Date, nullable=False)

    clan_id = db.Column(db.Integer, db.ForeignKey('clanovi.id'), nullable=True)
    clanarina_id = db.Column(db.Integer, db.ForeignKey('clanarine.id'), nullable=True)

class Treninga(db.Model):
    __tablename__ = 'treninzi'
    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.Date, nullable=False)
    opis = db.Column(db.String(50), nullable=False)

    clan_id = db.Column(db.Integer, db.ForeignKey('clanovi.id'), nullable=False)
    trener_id = db.Column(db.Integer, db.ForeignKey('treneri.id'), nullable=False)