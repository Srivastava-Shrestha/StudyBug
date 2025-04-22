# StudyBug/app/models/course.py

from .. import db

class Course(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String, default="courses.png")

    chapters = db.relationship('Chapter', back_populates='course', cascade='all, delete-orphan')
    enrolls = db.relationship('Enroll', back_populates='course', uselist=True , cascade='all, delete-orphan')



    