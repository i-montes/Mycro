from config.config import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    lastname = db.Column(db.String(250))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))