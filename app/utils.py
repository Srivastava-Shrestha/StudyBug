# StudyBug/app/utils.py
 
from flask import session
from .models import Admin,User

HOST = "http://127.0.0.1:1437"

def user_admin_checker():
    username = session.get("username")
    is_admin = Admin.query.filter_by(username=username).first()
    is_user = User.query.filter_by(username=username).first()

    if bool(is_admin):
        return 1
    elif bool(is_user):
        return 2
    else:
        return 0
    
def user_getter():
    username = session.get("username")
    is_user = User.query.filter_by(username=username).first()
    return is_user