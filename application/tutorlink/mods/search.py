# # Handles searching/browsing related pages
# Jeremy W, Lars S, Abel S, Brandon W
# App State
from tutorlink import app
from tutorlink.db.models import Subject, Tutor

# Libs
from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, validators


# # # Form layouts
class search_form(FlaskForm):
    search_subject = SelectField("Subject")
    search_term = StringField(
        "Search Term",
        validators=[validators.length(max=40)]
    )
    search_submit = SubmitField(
        "Search"
    )

# Creates form with dropdown options pre-filled
def new_form():
    form = search_form()

    # Populate subjects to DB
    # Possible TODO, optimize this
    subj = ["All Subjects"]
    for i in Subject.query.all():
        subj.append(i.subj_short)
    form.search_subject.choices = subj
    return form

# Makes form available for navbar to generate
app.jinja_env.globals.update(search_form=new_form)


# # # Routes
# GET -> Redirect to homepage for base search bar
# POST -> View results
@app.route("/search", methods=['GET','POST'])
def search_page():
    # Create form
    form = new_form()

    # Form submit | Returns search results
    if form.validate_on_submit():
        # Get list of tutors
        # Filter By Subject if needed
        res = Tutor.query.join(Subject)

        # Add subject to query if applicable
        if form.search_subject.data != "All Subjects":
            # Get the subject id
            # subj = Subject.query.filter_by(subj_short=form.search_subject.data).first()
            # append subject restriction to query
            res = res.filter( Subject.subj_short==form.search_subject.data)

        # Like search based off of search term if it exists
        if form.search_term.data != "":
            res = res.filter(
                Tutor.tutor_name.like("%" + form.search_term.data + "%") |
                Tutor.tutor_bio.like("%" + form.search_term.data + "%") |
                Tutor.tutor_subj_num.like("%" + form.search_term.data + "%") |
                Subject.subj_short.like("%" + form.search_term.data + "%") |
                Subject.subj_long.like("%" + form.search_term.data + "%")
            )

        # Preform Query
        res = res.all()

        # Render search page with result
        return render_template("search.jinja2", res=res, subj_db=Subject, search_term=form.search_term.data)
    elif len(form.search_term.data) > 40:
        flash(f"Entered search term is too long ({len(form.search_term.data)} > 40)")
    
    return redirect(url_for("index"))

# Allows for pre-filled subject when searching via navbar
@app.route("/search/<string:subject>", methods=['GET'])
def subject_search(subject):
    # Get list of tutor
    # Filter By Subject if needed
    res = Tutor.query.join(Subject)

    # Add subject to query from URL
    res = res.filter(Subject.subj_short == subject)

    # Preform Query
    res = res.all()

    # Render search page with result
    return render_template("search.jinja2", res=res, subj_db=Subject)

