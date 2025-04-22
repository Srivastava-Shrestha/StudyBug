# StudyBug/app/routes/dashboard.py

from flask import Blueprint, render_template, request, redirect, url_for,session
import requests
from ..models import User,Admin,Enroll,Attempt,Quiz,Course,Chapter
from ..utils import user_admin_checker, HOST, user_getter
from ..api import CourseApi
import os
from ..config import Configuration
import time
from .. import db
from datetime import datetime
import pytz

dashboard_bp = Blueprint("dashboard_bp",__name__)

@dashboard_bp.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if request.method == "GET":
        found_user = user_admin_checker()
        if found_user == 1:
            no_of_users = User.query.count()
            no_of_courses = Course.query.count()
            no_of_chapters = Chapter.query.count()
            no_of_quizz = Quiz.query.count()

            attempted = Attempt.query.filter_by(is_attempt=True).count()
            not_attempted = Attempt.query.filter_by(is_attempt=False).count()
            if attempted + not_attempted > 0:
                attempted_percentage = (attempted/(attempted+not_attempted))*100
                pie_list = [attempted_percentage, (100-attempted_percentage)]
            else:
                pie_list = [0,0]

            stats_list = [no_of_users,no_of_courses,no_of_chapters/no_of_courses,no_of_quizz]

            return render_template("admin_dashboard.html",stats_list=stats_list,pie_list=pie_list, active_page="home")
        elif found_user == 2:
            response = requests.get(f"{HOST}/api/course")
            if response.status_code == 200:
                course_list = response.json()
            else:
                course_list = []
            user = user_getter()
            user_id = user.user_id
            enroll_courses = Enroll.query.filter_by(user_id=user_id).all()
            enroll_courses_id = [each.course_id for each in enroll_courses]
            attempted = Attempt.query.filter_by(user_id=user_id,is_attempt=True).all()
            score_list = [attempt.result for attempt in attempted ]
            user_attempt = Attempt.query.filter_by(user_id=user_id,is_attempt=True).count()
            user_not_attempt = Attempt.query.filter_by(user_id=user_id,is_attempt=False).count()
            if user_attempt + user_not_attempt > 0:
                overall_list = [
                    (user_attempt / (user_attempt + user_not_attempt)) * 100,
                    100 - (user_attempt / (user_attempt + user_not_attempt)) * 100]
            else:
                overall_list = [0, 0] 
            
            return render_template("user_dashboard.html",course_list=course_list,enroll_courses_id=enroll_courses_id,score_list=score_list,overall_list=overall_list, active_page="home")
        else:
            return redirect(url_for("auth_bp.login"))
    


    if request.method == "POST":
        found_user = user_admin_checker()
        if found_user == 1:
            return render_template("admin_dashboard.html", active_page="home")
        elif found_user == 2:
            data = request.form
            method = data.get("_method")
            # Enroll
            if method == "enroll":
                course_id = data.get("course_id")
                user = user_getter()
                try:
                    new_enroll = Enroll(course_id=course_id, user_id=user.user_id)
                    db.session.add(new_enroll)
                    db.session.commit()
                    return redirect(url_for("dashboard_bp.course"))
                except:
                    db.session.rollback()
                    return redirect(url_for("dashboard_bp.dashboard"))
            # SEARCH
            elif method == "search":
                name = data.get("name")
                response = requests.get(f"{HOST}/api/course?name={name}")
                if response.status_code == 200:
                    course_list = response.json()
                user = user_getter()
                user_id = user.user_id
                enroll_courses = Enroll.query.filter_by(user_id=user_id).all()
                enroll_courses_id = [each.course_id for each in enroll_courses]
                attempted = Attempt.query.filter_by(user_id=user_id,is_attempt=True).all()
                score_list = [attempt.result for attempt in attempted ]
                user_attempt = Attempt.query.filter_by(user_id=user_id,is_attempt=True).count()
                user_not_attempt = Attempt.query.filter_by(user_id=user_id,is_attempt=False).count()
                if user_attempt + user_not_attempt > 0:
                    overall_list = [
                        (user_attempt / (user_attempt + user_not_attempt)) * 100,
                        100 - (user_attempt / (user_attempt + user_not_attempt)) * 100]
                else:
                    overall_list = [0, 0] 
                
                return render_template("user_dashboard.html",course_list=course_list,enroll_courses_id=enroll_courses_id,score_list=score_list,overall_list=overall_list, active_page="home")
        
        else:
            return redirect(url_for("auth_bp.login"))


            
@dashboard_bp.route("/dashboard/course", methods=["GET", "POST"])
def course():
    if request.method == "GET":
        found_user = user_admin_checker()
        if found_user == 1:
            response = requests.get(f"{HOST}/api/course")

            if response.status_code == 200:
                courses_list = response.json()  
            else:
                courses_list = []  
            return render_template("admin_course.html",courses_list=courses_list, active_page="course")
        elif found_user == 2:
            user = user_getter()
            courses = [enroll.course for enroll in user.enrolls]
            return render_template("user_course.html", enroll_courses=courses, active_page="course")
        else:
            return redirect(url_for("auth_bp.login"))
    
    elif request.method == "POST":
            found_user = user_admin_checker()
            if found_user == 1:
                data = request.form
                method = data.get("_method")

                # DELETE
                if method == "delete":
                    course_id = data.get("course_id")
                    if course_id:
                        get_course = url_for("courseapi",id=course_id,_external=True)
                        response = requests.delete(get_course)
                        if response.status_code == 200:
                            return redirect(url_for("dashboard_bp.course"))
                        else:
                            return {"message": "Failed to delete course!"}, response.status_code
                    else:
                        return {"message": "Course ID required!"}, 400
                
                # CREATE
                elif method == "create":
                    name = data.get("name")
                    description = data.get("description")
                    image = request.files.get("image") 
                    json={"name":name,"description":description}
                    if image:
                        u_image =f"{int(time.time())}_{image.filename}"
                        image_url = os.path.join(Configuration.UPLOAD_FOLDER, u_image)
                        image.save(image_url)
                        json["image"] = u_image

                    response = requests.post(f"{HOST}/api/course",json=json)
                    if response.status_code == 201:
                        return redirect(url_for("dashboard_bp.course"))
                
                # EDIT
                elif method == "edit":
                    course_id = data.get("course_id")
                    name = data.get("name")
                    description = data.get("description")
                    json = {"name":name, "description":description}

                    response = requests.put(f"{HOST}/api/course/{course_id}", json=json)
                    if response.status_code == 200:
                        return redirect(url_for("dashboard_bp.course"))
                    
                # SEARCH
                elif method == "search":
                    name = data.get("name")
                    print(name)
                    response = requests.get(f"{HOST}/api/course?name={name}")
                    if response.status_code == 200:
                        courses_list = response.json()
                        print(courses_list)
                        return render_template("admin_course.html", courses_list=courses_list ,active_page = "course")
                    
    
               
            elif found_user == 2:
                return render_template("user_course.html", active_page="course")
            else:
                return redirect(url_for("auth_bp.login"))
            

@dashboard_bp.route("/dashboard/course/<int:course_id>", methods=["GET","POST"])
@dashboard_bp.route("/dashboard/course/<int:course_id>/<int:chapter_id>", methods=["GET", "POST"])
def course_details(course_id,chapter_id=None):
    if request.method == "GET":
        found_user = user_admin_checker()
        if found_user == 1:
            response = requests.get(f"{HOST}/api/course/{course_id}")
            

            if response.status_code == 200:
                course = response.json()
            else:
                course = []  
            return render_template("admin_chapter.html", course=course, active_page="course")

        elif found_user == 2:

            response = requests.get(f"{HOST}/api/course/{course_id}")
            if response.status_code == 200:
                course = response.json()
                if chapter_id:
                    response2 = requests.get(f"{HOST}/api/chapter/{chapter_id}")
                    if response2.status_code == 200:
                        chapter = response2.json()
                        print(chapter)
                        return render_template("user_course_detail.html", course=course, chapter=chapter,current_chapter=chapter_id)
                    else:
                        return render_template("404.html")
                else:
                    return render_template("user_course_detail.html", course=course)
            else:
                return render_template("404.html")

        else:
            return redirect(url_for("auth_bp.login"))
        
    if request.method == "POST":
        found_user = user_admin_checker()
        if found_user == 1:
            data = request.form
            method = data.get("_method")


            #DELETE
            if method == "delete":
                chapter_id = data.get("chapter_id")
                if chapter_id:
                    response = requests.delete(f"{HOST}/api/chapter/{chapter_id}")
                    if response.status_code == 200:
                                return redirect(url_for("dashboard_bp.course_details",course_id=course_id))
                    else:
                        return {"message": "Failed to delete chapter!"}, response.status_code
                else:
                    return {"message": "Chapter ID required!"}, 400
                
            #CREATE
            elif method == "create":
                name = data.get("name")
                description = data.get("description")
                video = data.get("video")
                json = {"name":name, "description":description,"course_id":course_id, "video":video}
                response = requests.post(f"{HOST}/api/chapter",json=json)
                if response.status_code == 201:
                    return redirect(url_for("dashboard_bp.course_details", course_id=course_id))

            
            #EDIT
            elif method == "edit":
                chapter_id = data.get("chapter_id")
                name = data.get("name")
                description = data.get("description")
                video = data.get("video")
                json = {"name":name, "description":description, "video":video}
                response = requests.put(f"{HOST}/api/chapter/{chapter_id}", json=json)
                if response.status_code == 200:
                    return redirect(url_for("dashboard_bp.course_details", course_id=course_id))

            
        if found_user == 2:
           return render_template("user_course.html", active_page="course")
        else:
            return redirect(url_for("auth_bp.login"))

@dashboard_bp.route("/dashboard/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "GET":
        found_user = user_admin_checker()
        if found_user == 1:
                response1 = requests.get(f"{HOST}/api/course")
                if response1.status_code == 200:
                    courses_list = response1.json() 
                else:
                    courses_list = []

                response = requests.get(f"{HOST}/api/quiz")
                if response.status_code == 200:
                    chapter_details = response.json()
                    return render_template("admin_quiz.html",chapter_details=chapter_details,courses_list=courses_list, active_page = "quiz")
                else:
                    return render_template("404.html")
        elif found_user == 2:
            user = user_getter()
            attempts = user.attempts
            ist = pytz.timezone('Asia/Kolkata')
            today = datetime.now(ist).date()
            print(today)
            quizzes = [attempt.quiz  for attempt in attempts if not attempt.is_attempt and ist.localize(attempt.quiz.quiz_date).date()>=today]
            return render_template("user_quiz.html",quizzes=quizzes, active_page = "quiz")
        else:
            return redirect(url_for("auth_bp.login"))
        
    if request.method == "POST":
        found_user = user_admin_checker()
        if found_user == 1:
            data = request.form
            method = data.get("_method")

            #DELETE
            if method == "delete":
                quiz_id = data.get("quiz_id")
                if quiz_id:
                    response = requests.delete(f"{HOST}/api/quiz/{quiz_id}")
                    if response.status_code == 200:
                            return redirect(url_for("dashboard_bp.quiz",quiz_id=quiz_id))
                    else:
                        return {"message": "Failed to delete quiz!"}, response.status_code
                else:
                    return {"message": "Quiz ID required!"}, 400
            #EDIT
            elif method == "edit":
                quiz_id = data.get("quiz_id")
                title = data.get("title")
                quiz_date = data.get("quiz_date")
                duration = data.get("duration")
                json = {"title":title, "quiz_date":quiz_date, "duration":duration}
                response = requests.put(f"{HOST}/api/quiz/{quiz_id}", json=json)
                if response.status_code == 200:
                    return redirect(url_for("dashboard_bp.quiz"))
                
            #CREATE
            elif method == "create":                
                chapter_id = data.get("chapter_id")
                title = data.get("title")
                quiz_date = data.get("quiz_date")
                duration = data.get("duration")
                quiz_details = {"title":title, "quiz_date":quiz_date, "duration":duration, "chapter_id":chapter_id}
                response2 = requests.post(f"{HOST}/api/quiz",json=quiz_details)
                if response2.status_code == 201:
                    return redirect(url_for("dashboard_bp.quiz"))
                else:
                    return render_template("404.html")

        elif found_user == 2:
            return render_template("404.html")
        else:
            return redirect(url_for("auth_bp.login"))

@dashboard_bp.route("/dashboard/quiz/<int:quiz_id>", methods = ["GET", "POST"])
def questions(quiz_id):
    if request.method == "GET":
        found_user = user_admin_checker()
        if found_user == 1:
            response = requests.get(f"{HOST}/api/quiz/{quiz_id}")
            if response.status_code == 200:
                quiz_details = response.json()
                return render_template("admin_questions.html", quiz_details=quiz_details)
            else:
                return render_template("404.html")

        elif found_user == 2:
            return render_template("404.html")
        else:
            redirect(url_for("auth_bp.login"))

    elif request.method == "POST":
        found_user = user_admin_checker()
        if found_user == 1:
            data = request.form 
            method = data.get("_method")

            #DELETE
            if method == "delete":
                question_id = data.get("question_id")
                response = requests.delete(f"{HOST}/api/question/{question_id}")
                if response.status_code == 200:
                    return redirect(url_for("dashboard_bp.questions",quiz_id=quiz_id))
                else:
                    return {"message": "Failed to delete chapter!"}, response.status_code
        
            #EDIT
            elif method == "edit":
                question_id = data.get("question_id")
                statement = data.get("statement")
                option1 = data.get("option1")
                option2 = data.get("option2")
                option3 = data.get("option3")
                option4 = data.get("option4")
                correct_option = data.get("correct_option")
                json = {"statement":statement, "option1":option1, "option2":option2, "option3":option3, "option4":option4, "correct_option":correct_option}
                response = requests.put(f"{HOST}/api/question/{question_id}", json=json)
                if response.status_code == 200:
                    return redirect(url_for("dashboard_bp.questions", quiz_id=quiz_id))
                else:
                    return render_template("404.html")
                
            #CREATE
            elif method == "create":
                statement = data.get("statement")
                option1 = data.get("option1")
                option2 = data.get("option2")
                option3 = data.get("option3")
                option4 = data.get("option4")
                correct_option = data.get("correct_option")
                json = {"quiz_id":quiz_id,"statement":statement, "option1":option1, "option2":option2, "option3":option3, "option4":option4, "correct_option":correct_option}
                response = requests.post(f"{HOST}/api/question",json=json)
                if response.status_code == 201:
                    return redirect(url_for("dashboard_bp.questions",quiz_id=quiz_id))
                else:
                    return render_template("404.html")

        elif found_user == 2:
            return render_template("404.html")
        else:
            redirect(url_for("auth_bp.login"))

@dashboard_bp.route("/dashboard/quiz/<int:quiz_id>/attempt",methods=["GET","POST"])
def attempt(quiz_id):
    if request.method == "GET":
        found_user = user_admin_checker()
        if found_user == 1:
            return "HI"
        elif found_user == 2:
            response = requests.get(f"{HOST}/api/quiz/{quiz_id}")
            if response.status_code == 200:
                quiz = response.json()
                return render_template("user_attempt.html",quiz=quiz)
            else:
                render_template("404.html")
        else:
            return redirect(url_for("auth_bp.login"))
        
    elif request.method == "POST":
        found_user = user_admin_checker()
        if found_user == 1:
            return "hello"
        elif found_user == 2:
            data = request.form
            quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
            correct_options = [question.correct_option for question in quiz.questions]
            select_options = [int(value) for key,value in data.items()]
            marks = 0
            for i in range(len(correct_options)):
                if correct_options[i] == select_options[i]:
                    marks += 1 
            user = user_getter()
            user_id = user.user_id
            
            try:
                attempt = Attempt.query.filter_by(user_id=user_id,quiz_id=quiz_id).first()
                attempt.is_attempt = True
                attempt.result = round((marks/len(correct_options))*100,2)
                db.session.commit()
                return render_template("user_feedback.html",correct_options=correct_options,select_options=select_options,quiz=quiz,result=attempt.result)
            except:
                return "will handle later"
        else:
            return redirect(url_for("auth_bp.login"))
        

@dashboard_bp.route("/dashboard/result")
def result():
    if request.method == "GET":
        found_user = user_admin_checker()
        if found_user == 1:
            return "Hello"
        elif found_user == 2:
            user = user_getter()
            user_id = user.user_id
            try:
                result = Attempt.query.filter_by(user_id = user_id,is_attempt=True).all()
                return render_template("user_result.html",result=result,active_page="result")

            except:
                return "Will handle later"
        else:
            return redirect(url_for("auth_bp.login"))


@dashboard_bp.route("/dashboard/users", methods = ["GET","POST"])
def users():
    if request.method == "GET":
        found_user = user_admin_checker()
        if found_user == 1:
            try:
                users = User.query.all()
                return render_template("admin_user.html",users=users, active_page = "users")
            except:
                return render_template("404.html")


        elif found_user ==2:
            return render_template("404.html")
        else:
            redirect(url_for("auth_bp.login"))

    elif request.method == "POST":
        found_user = user_admin_checker()
        if found_user == 1:
            data = request.form
            method = data.get("_method")
            #DELETE
            if method == "delete":
                user_id = data.get("user_id")
                try:
                    user = User.query.filter_by(user_id = user_id).first()
                    if user:
                        db.session.delete(user)
                        db.session.commit()
                        return redirect(url_for("dashboard_bp.users"))
                    else:
                        return render_template("404.html")
                except:
                    db.session.rollback()
                    return {"message":"Something went wrong!"}
                
            #SEARCH
            if method == "search":
                username = data.get("username")
                try:
                    users = User.query.filter(User.username.like(f"%{username}%")).all()
                    return render_template("admin_user.html", users=users, active_page="users")
                except:
                    return render_template("404.html")

        elif found_user == 2:
            return "hi"
        else:
            return redirect(url_for("auth_bp.login"))



