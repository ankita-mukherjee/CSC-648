# # Handles display a tutor profile
# Abel S, Jeremy W, Ankita M
# app
from tutorlink import app
from tutorlink.db.db import db 
from tutorlink.db.models import Subject, Tutor, Tutor_Request

# flask-libs
from flask import redirect, render_template, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from flask_login import current_user
# libs
import re
from uuid import uuid4
from os import makedirs, path

class tutor_app_form(FlaskForm):
    name = StringField("Full Name", render_kw={"placeholder": "Full Name"})
    bio = TextAreaField("Bio", render_kw={"placeholder": "Your bio..."})
    subjects = SelectField("Subjects", choices=[])
    subject_num = StringField("Subject Number", render_kw={"placeholder": "Class"})
    video = StringField("Video Link (YouTube)", render_kw={"placeholder": "Video Link"})
    cv_file = FileField("Upload CV/Flyer (.pdf)", render_kw={"class": "app-file"})
    pic_file = FileField("Upload Photo (.jpg)", render_kw={"class": "app-file"})
    submit = SubmitField("Apply", render_kw={"class": "btn"})


# Tutor Application Route
@app.route('/tutor/register', methods=['GET', 'POST'])
def tutor_app_page():
    # Load form
    form = tutor_app_form()

    # Populate form with subject data
    subj = []
    for i in Subject.query.all():
        subj.append(i.subj_short)
    form.subjects.choices = subj

    # Apply tutor application
    if form.validate_on_submit():
        # TODO : Store info if not logged in

        # Redirect to login page if not logged in
        if not current_user.is_authenticated:
            flash("You must be signed-in to apply as Tutor")
            return redirect(url_for('login_page'))

        # Assume validation in debug mode
        # Else push to request db
        tutor = None
        if(app.debug):
            tutor = Tutor()
        else:
            tutor = Tutor_Request()

        # Populate tutor app object to be pushed to db
        # Only populates first run data
        tutor.tutor_name = form.name.data
        tutor.tutor_bio = form.bio.data
        if(form.video.data == ""):
            tutor.tutor_vid = None
        else:
            tutor.tutor_vid = form.video.data
        # Special Case for subject
        tutor.tutor_subj = int(Subject.query.filter_by(subj_short=form.subjects.data).first().subj_id)
        tutor.tutor_subj_num = form.subject_num.data

        # Get current user for user value
        tutor.tutor_user = current_user.user_id

        # File upload
        static_path = ""
        if app.debug:
            static_path = "tutorlink/static/tutors/"
        else: 
            static_path = "/var/www/application/tutorlink/static/tutors/"
        # Gen UUID for profile folder for file upload
        file_dir = str(uuid4())

        # UUID Collision checking and regen
        # I know its technically unneeded but /shrug
        while(path.exists(static_path + file_dir)):
            file_dir = str(uuid4())

        # Make tutor director
        makedirs(path.join(static_path, file_dir))
        
        # Picture upload
        # No file uploaded case
        if form.pic_file.data == None:
            tutor.tutor_photo = None
        elif not '.jpg' in form.pic_file.data.filename:
            tutor.tutor_photo = None
        # Photo provided
        else:
            tutor.tutor_photo = file_dir
            form.pic_file.data.save(path.join(static_path, file_dir, "photo.jpg"))
        
        # CV/Flyer upload
        # No file uploaded case
        if form.cv_file.data == None:
            tutor.tutor_cv = None
        elif not '.pdf' in form.cv_file.data.filename:
            flash("Incorrect File Type (should be .pdf)")
            tutor.tutor_cv = None
        # Photo provided
        else:
            tutor.tutor_cv = file_dir
            form.cv_file.data.save(path.join(static_path, file_dir, "cv.pdf"))

        # Push to DB
        db.session.add(tutor)
        db.session.commit()

        # redirect to tutor page if in debug
        if(app.debug):
            return redirect(url_for('tutor_profile', tutor_id=tutor.tutor_id))
        flash("Tutor Application Submitted")
        return redirect(url_for("index"))  
    
    # Return Registration form
    return render_template('tutor_app_template.jinja2', form=form)


# This is so that users can see the filename of the CV
def file_name_from_cv(tutor_cv):
    return re.search("[^\/]+$", tutor_cv).group(0)

# Makes function available for tutor.jinja2 to call
app.jinja_env.globals.update(cv_filename=file_name_from_cv)


# Returns page for specific tutor
@app.route("/tutor/view/<int:tutor_id>", methods=['GET'])
def tutor_profile(tutor_id):
    # Query for tutor to view
    tutor = Tutor.query.filter_by(tutor_id=tutor_id).first()
    # Redirect to index if not found
    if not tutor:
        flash("Tutor does not exist")
        return redirect(url_for('index'))
    # Display result
    return render_template("tutor.jinja2", tutor=tutor, subj_db=Subject)


