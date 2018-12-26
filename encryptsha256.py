import hashlib
import random
import string

secret = "uxc56.dyurtbgs"

def make_salt():
    letters = string.ascii_letters
    count = 0
    salt = ""
    while count < 5:
      c = random.choice(letters)  
      salt += c
      count += 1
    return salt

def make_userid_pw_hash(userid,pw,salt):
    final_string = userid+pw+salt
    final_string = final_string.encode("utf-8")
    return hashlib.sha256(final_string).hexdigest()

def make_userid_pw_secure_cookie_val(userid, pw):
    salt = make_salt()
    h = make_userid_pw_hash(userid,pw,salt)
    return "%s|%s"%(h,salt)

def check_userid_pw_cookie_val(val,userid,pw):
    if not userid or not pw or not val:
        return False
    hash_parts = val.split("|")
    hash = ""
    salt = ""
    new_hash = ""
    if hash_parts and len(hash_parts) > 1:
        hash = hash_parts[0]
        salt = hash_parts[1]
    if hash and salt:
        new_hash = make_hash(userid,pw,salt)
    if new_hash == hash:
        return True
    else:
        return False

"""
uses a default secret to create hash for the give input
"""
def make_hash(val):
    to_hash_string = str(val)+secret
    to_hash_string = to_hash_string.encode("utf-8")
    return hashlib.sha256(to_hash_string).hexdigest()
"""
uses a default secret to create a secure cookie val
"""
def make_secure_cookie_val(val):
    hash_val = make_hash(val)
    return "%s|%s"%(val,hash_val)

"""
verifies the given cookie val using the default secret
"""
def verify_cookie_val(cookie_val):
    is_valid = False
    parts = cookie_val.split("|")
    if parts and len(parts) > 1:
       if make_hash(parts[0]) == parts[1]:
           is_valid = True
    return is_valid

def verify_password(password,stored_password_hash):
    if make_hash(password) == stored_password_hash:
        return True
    else:
        return False
    
    
    
