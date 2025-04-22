# StudyBug/app/api/question.py

from flask import request
from flask_restful import Resource
from .. import db
from ..models import Quiz,Question

class QuestionApi(Resource):

    def post(self):
        data = request.get_json()
        quiz_id = data.get("quiz_id")
       
        try:
            question_exist = Quiz.query.filter_by(quiz_id=quiz_id).first()
            if question_exist:
                statement = data.get("statement")
                option1 = data.get("option1")
                option2 = data.get("option2")
                option3 = data.get("option3")
                option4 = data.get("option4")
                correct_option = data.get("correct_option")

                if statement is None or statement == "":
                    return {"message":"Statement is required!"}, 400
                if option1 is None or option1 == "":
                    return {"message":"Option 1 is required!"}, 400
                if option2 is None or option2 == "":
                    return {"message":"Option 2 is required!"}, 400
                if option3 is None or option3 == "":
                    return {"message":"Option 3 is required!"}, 400
                if option4 is None or option4 == "":
                    return {"message":"Option 4 is required!"}, 400
                if correct_option is None or correct_option == "":
                    return {"message":"Correct Option is required!"}, 400
                
                new_question = Question(quiz_id=quiz_id,statement=statement,option1=option1,option2=option2,option3=option3,option4=option4,correct_option=correct_option)
                db.session.add(new_question)
                db.session.commit()
                return {"message":"Question added successfully!"}, 201
            else:
                return {"message":"Quiz doesn't exist!"}, 400
        except Exception as e:
            db.session.rollback()
            return {"message":f"Something went wrong!{e}"}, 500
    
    def get(self,question_id=None):
        try:
            if question_id == None:
                question_details = Question.query.all()
                question_list = [{"statement":question.statement, 
                                  "option1":question.option1, 
                                  "option2":question.option2, 
                                  "option3":question.option3, 
                                  "option4":question.option4,
                                  "correct_option":question.correct_option,
                                  "quiz_id":question.quiz_id,
                                  "quiz":{"quiz_id":question.quiz.quiz_id, 
                                          "title":question.quiz.title, 
                                          "quiz_date":question.quiz.quiz_date.strftime("%Y-%m-%d"),
                                          "duration":question.quiz.duration}}
                                   for question in question_details]
                return question_list, 200

            else:
                question_exist = Question.query.filter_by(question_id=question_id).first()
                if question_exist:
                    question_details = {"statement":question_exist.statement,
                                    "option1":question_exist.option1,
                                    "option2":question_exist.option2,
                                    "option3":question_exist.option3,
                                    "option4":question_exist.option4,
                                    "correct_option":question_exist.correct_option}
                    return question_details, 200
                else:
                    return {"message":"Question not found"}, 400
        except Exception as e:
            return {"message":f"Something went wrong!"}, 500

    def put(self,question_id):

        try:
            question_exist = Question.query.filter_by(question_id=question_id).first()

            if question_exist:
                data = request.get_json()
                statement = data.get("statement")
                option1 = data.get("option1")
                option2 = data.get("option2")
                option3 = data.get("option3")
                option4 = data.get("option4")
                correct_option = data.get("correct_option")
                
                if statement:
                    question_exist.statement = statement
                if option1:
                    question_exist.option1 = option1
                if option2:
                    question_exist.option2 = option2
                if option3:
                    question_exist.option3 = option3
                if option4:
                    question_exist.option4 = option4
                if correct_option:
                    question_exist.correct_option = correct_option
                
                db.session.commit()
                return {"message":"Question updated successfully!"}, 200
            else:
                return {"message":"Question not found!"}, 400
            
        except Exception as e:
            db.session.rollback()
            return {"message":f"Something went wrong!{e}"}, 500
                
    def delete(self,question_id):
        try:
            question = Question.query.filter_by(question_id=question_id).first()
            if question:
                db.session.delete(question)
                db.session.commit()
                return {"message":"Question deleted successfully!"}, 200
            else:
                return {"message":"Question not found!"}, 400
            
        except:
            db.session.rollback()
            return {"message":"Something went wrong!"}, 500

