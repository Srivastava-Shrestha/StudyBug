# StudyBug/app/__init__.py

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy,session
from datetime import timedelta
from flask_restful import Api


app = Flask(__name__)
db = SQLAlchemy()

app.secret_key = "akss"
app.permanent_session_lifetime = timedelta(days=1)

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


def app_creator(MyConfig):

    from app.routes import home_bp,auth_bp,dashboard_bp
    from app.api import CourseApi, ChapterApi, QuizApi, QuestionApi

    app.config.from_object(MyConfig)
    db.init_app(app)
    api = Api(app)

    

    from app.models import User, Admin, Course, Chapter, Quiz, Enroll, Question, Attempt
    with app.app_context():
        db.create_all()

        if not Admin.query.filter_by(username="shrestha").first():
            admin=Admin(username="shrestha",email="shrestha@gmail.com")
            admin.set_password("shrestha30")
            db.session.add(admin)
            db.session.commit()

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    api.add_resource(CourseApi, '/api/course','/api/course/<int:id>')
    api.add_resource(ChapterApi, '/api/chapter', '/api/chapter/<int:chapter_id>')
    api.add_resource(QuizApi, '/api/quiz', '/api/quiz/<int:quiz_id>')
    api.add_resource(QuestionApi, '/api/question', '/api/question/<int:question_id>')

    app.run(debug=True, port=1437)
