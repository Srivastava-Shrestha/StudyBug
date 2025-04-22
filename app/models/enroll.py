# StudyBug/app/models/enroll.py

from .. import db

class Enroll(db.Model):
    __tablename__ = "enrolls"
    enroll_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)


    user = db.relationship('User', back_populates='enrolls', uselist=False)
    course = db.relationship('Course', back_populates='enrolls', uselist=False)