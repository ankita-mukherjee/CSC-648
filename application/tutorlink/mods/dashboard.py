from tutorlink import app
from tutorlink.db.models import Subject, Tutor, Message, User

# libs
from flask import render_template, redirect, url_for, flash
from flask_login import current_user


# # # Routes
@app.route("/dashboard", methods=['GET'])
def dashboard():
    # Redirect to login page if user not currently signed in
    if not current_user.is_authenticated:
        flash("You must be logged in to view your Dashboard")
        return redirect(url_for("login_page"))

    # Query database for user info to populate dashboard tabs with
    user = current_user.user_name  # TODO: remove this for method mentioned in dashboard.jinja2
    my_posts = Tutor.query.filter(Tutor.tutor_user == current_user.user_id).all()

    # Get user's sent/received messages in order of (most recent -> oldest)
    sent = Message.query.filter(Message.msg_student == current_user.user_id)
    sent = sent.order_by(Message.msg_id.desc()).all()
    received = Message.query.filter(Message.msg_tutor == current_user.user_id)
    received = received.order_by(Message.msg_id.desc()).all()

    return render_template('dashboard.jinja2', user=user, my_posts=my_posts, sent=sent,
                           received=received, tutor_db=Tutor, subj_db=Subject, user_db=User)
