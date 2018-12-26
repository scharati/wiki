
import re

def is_username_valid(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)

def is_password_valid(password):
    PW_RE = re.compile(r"^.{3,20}$")
    return PW_RE.match(password)

def is_email_valid(email):
    if(not email):
        return True
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EMAIL_RE.match(email)    