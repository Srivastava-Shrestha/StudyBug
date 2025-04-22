# StudyBug/app/api/course.py

from flask import request
from flask_restful import Resource
from .. import db
from ..models import Course
from ..config import Configuration
import os

class CourseApi(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        image = data.get("image")

        if name is None or name == "":
            return {"message": "Course Name is required!"}, 400
        if description is None or description == "":
            return {"message": "Description is required!"}, 400

        try:
            new_course = Course(name=name,description=description)
            if image is not None or image != "":
                new_course.image = image
            db.session.add(new_course)
            db.session.commit()
            return {"message": "Course added succesfully!"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Something went wrong!{e}"}, 500 
    
    def get(self,id=None):

        try:
            if id is None:
                name = request.args.get("name")
            
                all_course = Course.query
                if name:
                    all_course = all_course.filter(Course.name.like(f"%{name}%"))
                
                all_course = all_course.all()

                courses_list = [{"course_id":course.course_id, 
                                 "name": course.name, 
                                 "description": course.description, 
                                 "image": course.image, 
                                 "chapters": [
                            {
                                "chapter_id": chapter.chapter_id,
                                "name": chapter.name,
                                "description": chapter.description,
                                "course_id":id,
                                "url": chapter.video
                            }
                            
                        for chapter in course.chapters]} for course in all_course]
                return courses_list, 200

            else:
                course = Course.query.filter_by(course_id=id).first()
                if course:
                    course_details = {
                        "name": course.name,
                        "description": course.description,
                        "image": course.image,
                        "chapters": [
                            {
                                "chapter_id": chapter.chapter_id,
                                "name": chapter.name,
                                "description": chapter.description,
                                "course_id":id,
                                "url": chapter.video
                            }
                            
                        for chapter in course.chapters]
                    }
                    return course_details, 200
                else:
                    return {"message": "Course not Found"}, 400
            
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message":"Something went wrong!"}, 500      

    def put(self,id):

        try:
            data = Course.query.filter_by(course_id=id).first()
            if data:
                course = request.get_json()
                name = course.get("name")
                description = course.get("description")
                image = course.get("image")
                if name:
                    data.name = name

                if description:
                    data.description=description

                if image:
                    data.image = image
                    
                db.session.commit()
                return {"message":"Course updated successfully!"},200

            else:
                return {"message":"Course not found"}, 400
            
        except Exception as e:
            db.session.rollback()
            return {"message":f"Something went wrong{e}"}, 500
        
    def delete(self,id):
        
        try:
            course = Course.query.filter_by(course_id=id).first()
            if course:
                file_url = os.path.join(Configuration.UPLOAD_FOLDER, course.image)
                os.remove(file_url)
                db.session.delete(course)
                db.session.commit()
                return {"message":"Course deleted successfully!"}, 200
            else:
                return {"message":"Course not found!"}, 400
            
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message":f"Something went wrong!{e}"}, 500

                


            




        
        
        

        
        

        
        