# StudyBug/app/api/chapter.py

from flask import request
from flask_restful import Resource
from .. import db
from ..models import Chapter,Course

class ChapterApi(Resource):
    def post(self):
        data = request.get_json()
        course_id = data.get("course_id")

        course_exist = Course.query.filter_by(course_id=course_id).first()

        try:
            if course_exist:
                name = data.get("name")
                description = data.get("description")
                video = data.get("video")
                if name is None or name == "":
                    return {"message":"Name is required!"}, 400
                if description is None or description =="":
                    return {"message":"Description is required!"}, 400
                if video is None or video =="":
                    return {"message":"video is required!"}, 400
                
                new_chapter = Chapter(name=name,description=description,course_id=course_id,video=video)
                db.session.add(new_chapter)
                db.session.commit()
                return {"message":"Chapter added successfully!"}, 201
            
            else:
                return {"message":"Course doesn't Exist!"}, 400
            
        except :
            db.session.rollback()
            return {"message":"Something went wrong!"}, 500
                 
    def get(self,chapter_id=None):
        try:
            if chapter_id == None:
                all_chapters = Chapter.query.all()
                chapter_list = [{"chapter_id":chapter.chapter_id,
                                  "name":chapter.name,
                                   "description":chapter.description,
                                   "course_id":chapter.course_id,
                                   "video":chapter.video} for chapter in all_chapters]
                return chapter_list, 200
            else:
                data = Chapter.query.filter_by(chapter_id=chapter_id).first()
                if data:
                    chapter_details = {"chapter_id":chapter_id, 
                                       "name":data.name,
                                       "description":data.description,
                                       "course_id":data.course_id, 
                                       "video":data.video,
                                       }
                    return chapter_details, 200
                else:
                    return {"message":"Chapter not Found"}, 404
                
        except:
            return {"message":"Something went Wrong!"}, 500
        
    def put(self,chapter_id):
        
        try:
            chapter_details = Chapter.query.filter_by(chapter_id=chapter_id).first()
            if chapter_details:
                data = request.get_json()
                name = data.get("name")
                description = data.get("description")
    
                if name:
                    chapter_details.name = name
                if description:
                    chapter_details.description = description
                db.session.commit()
                return {"message":"Chapter updated successfully!"}, 200
            else:
                return {"message":"Chapter not found!"}, 400
        except:
            db.session.rollback()
            return {"message":"Something went wrong!"}, 500
        
    def delete(self,chapter_id):
        try:
            chapters = Chapter.query.filter_by(chapter_id=chapter_id).first()
            if chapters:
                db.session.delete(chapters)
                db.session.commit()
                return {"message":"Chapter deleted successfully!"}, 200
            else:
                return {"message":"Chapter not found!"}, 400
            
        except:
            db.session.rollback()
            return {"message":"Something went wrong!"}, 500
