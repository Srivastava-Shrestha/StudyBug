# StudyBug/app/models/chapter.py

from .. import db

class Chapter(db.Model):
    __tablename__="chapters"
    chapter_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    video = db.Column(db.String(100))

    course = db.relationship('Course', back_populates='chapters', uselist=False)
    quizzes = db.relationship('Quiz', back_populates='chapter' ,cascade='all, delete-orphan')
