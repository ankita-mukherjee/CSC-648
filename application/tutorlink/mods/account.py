# # Handles account management related functions
# Jeremy W, Lars S

from tutorlink import app, login_manager
from tutorlink.db.models import User
from tutorlink.db.db import db

# libs
from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask import flash
from flask_login import login_required, logout_user, login_user, current_user

# # Account Registration Page
class register_form(FlaskForm):
    username = StringField("Username")
    password = StringField("Password")
    email = StringField("Email")
    submit = SubmitField("Sign Up")

class login_form(FlaskForm):
    email = StringField("Email")
    password = StringField("Password")
    submit = SubmitField("Login")

# Register account to DB
# POST -> Submit Account Registration
# GET -> Get form for creating account
@app.route("/acc/register", methods=['POST','GET'])
def register_page():
    # Create form for user reg
    form = register_form()

    # Validate account creation
    # Push to db on success
    # Return error on failure
    if form.validate_on_submit():
        # Verify empty fields
        if form.email.data == "" or form.password.data == "" or form.username.data == "":
            flash("Error : Empty Field")
            # TODO: return form back to user with their details pre-filled
            return render_template("register_template.jinja2", form=form)

        # Verify SFSU Email
        if not form.email.data.lower().endswith("sfsu.edu"):
            flash("Error : Creating an account requires SFSU Email")
            return render_template("register_template.jinja2", form=form)
        
        # Verify PW requirements
        # TODO : This

        # Verify account doesn't already exist
        existing_user = User.query.filter_by(user_name=form.username.data).all()
        if len(existing_user) != 0:
            flash("Error: User already exists")
            return render_template("register_template.jinja2", form=form)
        
        # Verify email isn't already used
        existing_user = User.query.filter_by(user_email=form.email.data).all()
        if len(existing_user) != 0:
            flash("Error: Email already in use")
            return render_template("register_template.jinja2", form=form)

        # Create new user account object
        new_acc = User(
            user_name=form.username.data,
            user_email=form.email.data
        )
        # Hash and store password
        new_acc.set_password(form.password.data)

        # Push new user account to db
        db.session.add(new_acc)
        db.session.commit()

        # Redirect to login page for user login
        # Possible TODO autologin and redirect to home page

        # Return to index for redirect to home page
        flash("Account Created Successfully")
        return redirect(url_for("login_page"))

    # Return form for user creation
    return render_template("register_template.jinja2", form=form)



# # Account Login page
# GET -> Get Login page
#     -> Redirect to home if logged in
# Post -> Login
@app.route("/acc/login", methods=['POST','GET'])
def login_page():
    form = login_form()

    # Post -> User attempting to login
    if form.validate_on_submit():
        # Find user account
        login_acc = User.query.filter_by(user_email=form.email.data).first()

        # Validate login info
        if login_acc and login_acc.check_password(form.password.data):
            # Login user then redirect to index
            login_user(login_acc)
            return(redirect(url_for("index")))
        
        # Return case for failed login
        # TODO : Flash message of error and return login page
        flash('Invalid username/password combination')
#        return("Login Error")

    # Return login page
    return render_template('login_template.jinja2', form=form)
  
  
# Logout API
@app.route("/acc/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    flash("Logged Out")
    return redirect(url_for('login_page'))

# Login API
# User loader for login
@login_manager.user_loader
def user_loader(user_id):
    if user_id is not None:
        return User.query.filter_by(user_id=user_id).first()
    return None


# Gets user id of current user
def get_curr_user():
    if current_user.is_authenticated:
        return current_user.user_name
    return None


# Makes user checking function available for navbar to use
app.jinja_env.globals.update(get_curr_user=get_curr_user)


# # Debug Routes
if app.debug:
    @app.route('/acc/debug/login')
    @login_required
    def acc_debug_login():
        return("You are logged in!")

    @app.route("/acc/debug")
    def acc_debug():
        res = User.query.all()
        ret = ""
        for i in res:
            ret = ret + i.usr2str()
        return(ret)

