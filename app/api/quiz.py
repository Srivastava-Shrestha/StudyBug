# StudyBug/app/api/quiz.py

from flask import request
from flask_restful import Resource
from .. import db
from datetime import datetime
from ..models import Chapter,Quiz,Attempt

class QuizApi(Resource):
    def post(self):
        data = request.get_json()
        chapter_id = data.get("chapter_id")
        
        try:
            chapter_exist = Chapter.query.filter_by(chapter_id=chapter_id).first()

            if chapter_exist:
                
                title = data.get("title")
                quiz_date = data.get("quiz_date")
                duration = data.get("duration")

                if title is None or title == "":
                    return {"message":"Title is required!"}, 400
                if quiz_date is None or quiz_date == "":
                    return {"message":"Quiz date is required!"}, 400
                if duration is None or duration == "":
                    return {"message":"Duration is required"}, 400
                
                try:
                    quiz_date = datetime.strptime(quiz_date, "%Y-%m-%d").date()
                except ValueError:
                    return {"message": "Invalid date format! Use YYYY-MM-DD."}, 400
                
                new_quiz = Quiz(title=title,quiz_date=quiz_date,duration=duration,chapter_id=chapter_id)
                db.session.add(new_quiz)
                db.session.flush()
                chapter = Chapter.query.filter_by(chapter_id=chapter_id).first()
                enrolls = chapter.course.enrolls
                user_ids = [enroll.user_id for enroll in enrolls] 
                quiz_id = new_quiz.quiz_id
                for user_id in user_ids:
                    new_attempt = Attempt(user_id=user_id, quiz_id=quiz_id) 
                    db.session.add(new_attempt)              
                db.session.commit()
                return {"message":"Quiz added successfully!"}, 201
            else:
                return {"message":"Chapter doesn't exist!"}, 400
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message":"Something went wrong!"}, 500
    
    def get(self,quiz_id=None):

        try:
            if quiz_id == None:
                chapters_having_quizzes = Chapter.query.filter(Chapter.quizzes != None).all()
                data = [{
                    "name": chapter.name,
                    "quizzes": [{
                        "quiz_id": quiz.quiz_id,
                        "title":quiz.title, 
                        "quiz_date":quiz.quiz_date.strftime("%Y-%m-%d"),
                        "duration":quiz.duration
                    }for quiz in chapter.quizzes]
                }for chapter in chapters_having_quizzes]
                
                return data, 200
            else:
                quiz_exist = Quiz.query.filter_by(quiz_id=quiz_id).first()
                if quiz_exist:
                    quiz_details = {"title":quiz_exist.title,
                                    "quiz_date":quiz_exist.quiz_date.strftime("%Y-%m-%d"),
                                    "duration":quiz_exist.duration,
                                    "chapter_id":quiz_exist.chapter_id,
                                    "questions":[{"statement":question.statement, 
                                                  "question_id":question.question_id,
                                  "option1":question.option1, 
                                  "option2":question.option2, 
                                  "option3":question.option3, 
                                  "option4":question.option4,
                                  "correct_option":question.correct_option}for question in quiz_exist.questions]
                                    }
                    return quiz_details, 200
                else:
                    return {"message":"Quiz not found"}, 400
        except Exception as e:
            return {"message":f"Something went wrong!{e}"}, 500

    def put(self,quiz_id):

        try:
            quiz_exist = Quiz.query.filter_by(quiz_id=quiz_id).first()

            if quiz_exist:
                data = request.get_json()
                title = data.get("title")
                quiz_date = data.get("quiz_date")
                duration = data.get("duration")
                
                if title:
                    quiz_exist.title = title
                if quiz_date :
                    try:
                     quiz_date = datetime.strptime(quiz_date, "%Y-%m-%d").date()
                    except ValueError:
                     return {"message": "Invalid date format! Use YYYY-MM-DD."}, 400
                    quiz_exist.quiz_date = quiz_date
                if duration:
                    quiz_exist.duration = duration
                db.session.commit()
                return {"message":"Quiz updated successfully!"}, 200
            else:
                return {"message":"Quiz not found!"}, 400
            
        except Exception as e:
            db.session.rollback()
            return {"message":f"Something went wrong!{e}"}, 500
                
    def delete(self,quiz_id):
        try:
            quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
            if quiz:
                db.session.delete(quiz)
                db.session.commit()
                return {"message":"Quiz deleted successfully!"}, 200
            else:
                return {"message":"Quiz not found!"}, 400
            
        except:
            db.session.rollback()
            return {"message":"Something went wrong!"}, 500


