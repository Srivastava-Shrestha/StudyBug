#StudyBug/app/model/attempt.py

from .. import db

class Attempt(db.Model):
    __tablename__ = "attempt"
    attempt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    is_attempt = db.Column(db.Boolean, default=False)
    result = db.Column(db.Integer)

    user = db.relationship('User', back_populates='attempts', uselist=False)
    quiz = db.relationship('Quiz', back_populates='attempts', uselist=False)