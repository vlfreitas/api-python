from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    requestQuantity = db.Column(db.Integer)

    def __init__(self, username, email, requestquantity=50):
        self.username = username
        self.email = email
        self.requestQuantity = requestquantity