from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    requestQuantity = db.Column(db.Integer)

    def __init__(self, username, email, requestquantity):
        self.username = username
        self.email = email
        self.requestQuantity = requestquantity

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def from_dict(self, data):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'requestQuantity': self.requestQuantity,
            "email": self.email
        }
        return data
