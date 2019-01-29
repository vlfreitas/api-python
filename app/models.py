from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username
        }
        if include_email:
            data['email'] = self.email
        return data