# StudyBug/app/models/quiz.py

from .. import db

class Quiz(db.Model):
    __tablename__ = "quizzes"
    quiz_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.chapter_id'), nullable=False)
    title = db.Column(db.String(35), nullable=False)
    quiz_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    chapter = db.relationship('Chapter', back_populates='quizzes', uselist=False)
    questions = db.relationship('Question', back_populates='quiz',cascade='all, delete-orphan')
    attempts = db.relationship('Attempt', back_populates='quiz',cascade='all, delete-orphan')
  

