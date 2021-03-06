from flask import Flask 
from flask import render_template, redirect, url_for
from flask import request
import pdb
import encryptsha256
from flask import session as login_session
import dbservice
import hashlib
from functools import wraps
import validation

app = Flask(__name__)


def login_required( f ):
    @wraps( f )
    def wrapper_func(*args, **kwargs):
        if "logged_in_user" not in login_session:
            return redirect( url_for("show_landing_page") )
        else:
            return f(*args, **kwargs)
    return wrapper_func
  

def authorization_required( f ):
    @wraps( f )
    def wrapper_func(*args, **kwargs):
        for key in kwargs:
            if key == "title":
                title_val = kwargs.get("title")
                page = dbservice.get_wikipage_by_title( title_val )
                page_owner_id = page.owner
                login_user = get_login_user()
                if page_owner_id == login_user.id:
                    return f(*args, **kwargs)
        return  redirect( url_for("show_landing_page") )
    return wrapper_func

# routes
@app.route("/login")
def show_login_page():
    return render_template("login.html")

@app.route("/authenticate", methods = ['POST'])
def authenticate_user():
    try:
        user_name = request.form['user_name']
        user_pwd = request.form['user_password']
        app.logger.info("++++ user_name ++++")
        app.logger.info( user_name )
        app.logger.info("++++ password ++++")
        app.logger.info( user_pwd )
        # get the user record from database 
        # check the password and if it matches then
        # create a cookie
        # store the session ?
        user = dbservice.get_user_by_name( user_name )
        app.logger.info("+++ user is +++");
        app.logger.info(user)
        if user:
            input_pwd_hash = encryptsha256.make_hash( user_pwd )
            stored_pwd_hash = user.pwdhash
            if input_pwd_hash == stored_pwd_hash:
                app.logger.info("+++ Passwords matched +++")
                login_session["logged_in_user"] = user.username
                cookie = make_login_cookie(user.id, user_pwd)
                wikipages = dbservice.get_all_wikipages()
                resp = app.make_response(redirect( url_for( "show_landing_page" )))
                resp.set_cookie("mywiki-credentials", cookie )
                return resp
            else:
                return redirect( url_for("show_login_page") )
        else:
            return redirect( url_for("show_login_page") )
    except Exception, e:
        app.logger.info("authenticate_user: Exception occurred" + str(e))
        return redirect( url_for("show_login_page") )

@app.route("/")
def show_landing_page():
    user = get_login_user()
    wikipages = dbservice.get_all_wikipages()
    app.logger.info("pages are:")
    app.logger.info(wikipages)
    return render_template("index.html", user=user, pages=wikipages)

@app.route("/logout")
@login_required
def logout():
    del login_session["logged_in_user"]
    return redirect( url_for("show_landing_page") )

@app.route("/<title>")
def show_page( title ):
    try:
        user = get_login_user()
        page = dbservice.get_wikipage_by_title( title )
        if page:
            return render_template("page.html", user = user,  page = page)
        else:
            return render_template("new_page.html")
    except Exception, e:
         app.logger.info("show_page: Exception occurred" + str(e))
         return render_template( "new-page.html", title = title )


@app.route("/edit/<title>")
@login_required
@authorization_required
def show_edit_page( title ):
    app.logger.info("+++ title is +++")
    app.logger.info( title )
    page = dbservice.get_wikipage_by_title( title )
    app.logger.info("+++ page content is : +++")
    app.logger.info(page.content)
    if page:
        return render_template("edit-page.html", page = page )
    else:
        return redirect( url_for("show_landing_page") )

@app.route("/editcomplete" , methods = ["POST"])
def complete_edit_page():
    title = request.form.get("page-title")
    app.logger.info("+++ complete_edit_page : title +++")
    app.logger.info( title )
    new_content = request.form.get("page-content")
    page = dbservice.get_wikipage_by_title( title )
    user = get_login_user()
    if page:
        page.content = new_content
    return render_template( "page.html", user = user, page = page)

@app.route("/new/<title>" , methods = ["POST"])
@login_required
def create_page( title ):
    content =  request.form['page-content']
    app.logger.info(" +++ content is +++ ")
    app.logger.info( content )
    logged_in_user = login_session.get("logged_in_user")
    app.logger.info("+++ logged in user: +++")
    logged_in_user = user = dbservice.get_user_by_name( "user1@hamsa.org")
    app.logger.info(logged_in_user)
    if content and logged_in_user:
        dbservice.create_wikipage(title, content.strip(), logged_in_user )
        return redirect( url_for( "show_landing_page" ) )
    return render_template( "new-page.html", title = title )

@app.route("/show-register-form")
def register_new_user():
    return render_template("register-user.html" )

@app.route("/createuser", methods= ["POST"] )
def create_user():
    errors = {}
    pdb.set_trace()
    email = request.form.get("user_name")
    password = request.form.get("user_password")
    confirm_password = request.form.get("confirm_password")
    if not validation.is_email_valid( email ):
        errors["email"] = "invalid e-mail"
    if not validation.is_password_valid( password ):
        errors["password"] = "incorrect password"
    if not password == confirm_password:
        errors["mismatch"] = "passwords did not match"
    if len(errors) > 0:
        return render_template("register-user.html", errors = errors)
    return redirect(url_for( "show_landing_page"))


def get_login_user():
    username = login_session.get("logged_in_user")
    user = None
    if username:
        user = dbservice.get_user_by_name( username )
    return user

def make_login_cookie(userid, password):
    pwd_string = password + app.secret_key
    pwd_string_hash = hashlib.sha256(pwd_string).hexdigest()
    return "%s|%s" % (userid, pwd_string_hash)

def verify_cookie_and_login( ):
    val = request.cookies.get('mywiki-credentials', None)
    print("+++ cookie-val is: +++")
    print( val )
    if val:
        parts = val.split("|")
        if len( parts ) == 2:
                user_id = parts[0]
                pwd_hash = parts[1]
                # get the user from db
                user =  dbservice.get_user_by_id( user_id )
                user_pwd_hash = user.pwdhash
                if user_pwd_hash == pwd_hash:
                    login_session['logged_in_user'] = user.username
                    return True
                else:
                    return False
    return False
                

# starting the server
if __name__ == '__main__':
    app.debug = True
    app.secret_key="ouxtcu143"
    app.run(host = "0.0.0.0", port = 5000)