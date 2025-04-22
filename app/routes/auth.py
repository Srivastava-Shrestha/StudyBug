# StudyBug/app/routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for,session
from ..models import User,Admin
from .. import db

auth_bp = Blueprint("auth_bp",__name__)

@auth_bp.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        data = request.form.to_dict()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        
        if username is None or username == "":
            return render_template("signup.html",message="Username is required!")
        if email is None or email == "":
            return render_template("signup.html", message="Email Address is required!")
        if password is None or password == "":
            return render_template("signup.html", message="Password is required!")
        if confirm_password is None or confirm_password == "":
            return render_template("signup.html", message="Confirm Password is required!")
        
        username = username.lower()
        email = email.lower()

        if len(username) < 3:
            return render_template("signup.html", message="Username must be minimum of 3 Characters!")

        if bool(User.query.filter_by(username=username).first()):
            return render_template("signup.html",message="This username is already in use!")
        if bool(User.query.filter_by(email=email).first()):
            return render_template("signup.html",message="This Email is already in use!")
        
        if len(password) < 8 or len(confirm_password) < 8:
            return render_template("signup.html",message="Password must be minimum of 8 Characters!")

        if password != confirm_password:
            return render_template("signup.html",message="Password and Confirm Password must be same!")

        try:
            
            new_user = User(username=username,email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth_bp.login"))
        except:
            db.session.rollback()
            return render_template("signup.html",message="Something went wrong!")
        
        

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        try:
            data = request.form.to_dict()
            username = data.get("username")
            password = data.get("password")

            if len(username) < 3:
                return render_template("login.html", message="Username must be minimum of 3 Characters!")
            if len(password) < 8:
                return render_template("login.html", message="Password must be minimum of 8 Characters!")
            
            username = username.lower()

            admin_checking = Admin.query.filter_by(username=username).first()
            user_checking = User.query.filter_by(username=username).first()
            if admin_checking:
                if admin_checking.check_password(password):
                    session.permanent = True

                    session["username"] = username
                    return redirect(url_for("dashboard_bp.dashboard"))
                else:
                    return render_template("login.html", message="Incorrect Username or Password!")
            elif user_checking:
                if user_checking.check_password(password):
                    session.permanent = True

                    session["username"] = username
                    return redirect(url_for("dashboard_bp.dashboard"))
                else:
                    return render_template("login.html", message="Incorrect Username or Password!")
            else:
                return render_template("login.html", message="Account doesn't Exist!")
            
        except Exception as e:
            return render_template("login.html", message=f"Something went wrong! {e}")
        


@auth_bp.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("auth_bp.login"))
    # return dir(session)

