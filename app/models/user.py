# StudyBug/app/models/user.py

from .. import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(30),nullable=False,unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(30))
    qualification = db.Column(db.String(25))
    dob = db.Column(db.DateTime)
    status = db.Column(db.String(10))

    enrolls = db.relationship('Enroll', back_populates='user',cascade='all, delete-orphan')
    attempts = db.relationship('Attempt',back_populates='user',cascade='all, delete-orphan')
   
    
    def set_password(self,password):
        hashed_password = generate_password_hash(password)
        self.password = hashed_password
        
    def check_password(self,password):
        return check_password_hash(self.password,password)
        
