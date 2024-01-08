# # Handles display a tutor profile
# app
from tutorlink import app
from tutorlink.db.db import db
from tutorlink.db.models import Subject, Tutor, Message, User

# libs
from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, validators
from flask_login import current_user


# # # Form layouts
# Messaging form created now so actual BE integration later will be less painful
class message_form(FlaskForm):
    message_body = TextAreaField(
        "Message Body",
        validators=[validators.length(max=512)],  # so that the message field is limited on user-side
        render_kw={"placeholder": "Please include your contact info so that the tutor can get back to you . . .",
                   "autofocus": "true"}
    )
    message_submit = SubmitField(
        "Send"
    )


# Used to get the message that was just created
def latest_message(user_id, tutor_id):
    query = Message.query.filter(Message.msg_student == user_id)
    query = query.filter(Message.msg_listing == tutor_id)
    msgs = query.all()
    return msgs[len(msgs) - 1]


# Test template for messaging page
@app.route("/message/tutor/<int:tutor_id>", methods=['GET', 'POST'])
def message_tutor(tutor_id):
    # Check tutor exists
    tutor = Tutor.query.filter(Tutor.tutor_id == tutor_id).first()
    if tutor is None:
        # TODO: Flash Message telling user that tutor does not exist
        flash("Tutor does not exist")
        return redirect(url_for("index"))

    # Create form
    form = message_form()

    # Form submit | Returns page with sent message
    if form.validate_on_submit():
        # Redirect to login page if user not currently signed in
        if not current_user.is_authenticated:
            flash("Login to send your message")
            # TODO: preserve contents of message for lazy registration
            return redirect(url_for("login_page"))

        # Create new message object
        new_msg = Message(
            msg_tutor=tutor.tutor_user,
            msg_student=current_user.user_id,
            msg_listing=tutor.tutor_id,
            msg_text=form.message_body.data
        )

        # Push new message to db
        db.session.add(new_msg)
        db.session.commit()

        # Redirect user to message they just sent/created
        flash("Message sent")
        msg_id = latest_message(current_user.user_id, tutor.tutor_id).msg_id
        return redirect(url_for("view_message", msg_id=msg_id))

    # Return form for message creation
    return render_template("send_message.jinja2", tutor=tutor, subj_db=Subject, form=form)


# Allows a user to view the messages they have sent or received
@app.route("/message/view/<int:msg_id>", methods=['GET'])
def view_message(msg_id):
    # Redirect to login page if user not currently signed in
    if not current_user.is_authenticated:
        flash("Login to view message")
        return redirect(url_for("login_page"))

    # Check message exists
    message = Message.query.filter(Message.msg_id == msg_id).first()
    if message is None:
        flash("Message does not exist")
        return redirect(url_for("dashboard"))

    # Check user is allowed to access the specified message
    if (message.msg_tutor != current_user.user_id) and (message.msg_student != current_user.user_id):
        flash("Message does not exist")
        return redirect(url_for("dashboard"))

    # Query DB to get info about the messaging parties
    student_user = User.query.filter(User.user_id == message.msg_student).first()
    tutor_post = Tutor.query.filter(Tutor.tutor_id == message.msg_listing).first()
    subject = Subject.query.filter_by(subj_id=tutor_post.tutor_subj).first().subj_short + ' ' + tutor_post.tutor_subj_num

    # Check if user is the sender or the receiver (for tab titling purposes)
    sender = None
    if current_user.user_id == student_user.user_id:
        sender = True
    elif current_user.user_id == tutor_post.tutor_user:
        sender = False

    # Return page with message details
    return render_template("view_message.jinja2", student=student_user, tutor=tutor_post,
                           subject=subject, message=message.msg_text, sender=sender)
