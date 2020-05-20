from FormEntry import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Pinfo(db.Model):
    citizenship = db.Column(db.Integer, nullable=False, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    sex = db.Column(db.String(3), nullable=False)
    picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    dob = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Pinfo('{self.firstname}', '{self.lastname}', '{self.sex}', '{self.dob}', '{self.picture}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    userinfo = db.relationship('Pinfo', backref='Entity')
 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

    
