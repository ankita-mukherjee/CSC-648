# # Database models
# Jeremy W
from tutorlink.db.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User model for database
# UserMixin, 
class User(UserMixin, db.Model): 
    __tablename__ = "user"
    # # #  Columns
    user_id = db.Column(
        db.Integer(),
        primary_key=True
    )
    user_name = db.Column(
        db.String(32),
        primary_key=False,
        nullable=False,
        unique=True
    )
    user_pw = db.Column(
        db.String(162),
        primary_key=False,
        nullable=False,
        unique=False
    )
    user_email = db.Column(
        db.String(64),
        primary_key=False,
        nullable=False,
        unique=True
    )
    # # # Util Functions
    # Generates hash and sets password in db
    def set_password(self, password):
        self.user_pw = generate_password_hash(password)
    
    # Check password against stored hash
    def check_password(self, password):
        return check_password_hash(self.user_pw, password)
    
    # Login id
    def get_id(self):
        return self.user_id

    # Simple print
    def __repr__(self):
        return "<User {}>".format(self.user_name)
    
    # Full data printing
    def usr2str(self):
        return f"===\nid:{self.user_id}\nun:{self.user_name}\npw:{self.user_pw}\nemail:{self.user_email}\n"

# Subject model to hold different subject names
class Subject(db.Model):
    __tablename__ = "subject"
    # # # Columns
    subj_id = db.Column(
        db.Integer(),
        primary_key=True
    )
    subj_short = db.Column(
        db.String(8),
        primary_key=False,
        nullable=False,
        unique=True
    )
    subj_long = db.Column(
        db.String(32),
        primary_key=False,
        nullable=False,
        unique=True
    )

    def __repr__(self):
        return "<Subject {}>".format(self.subj_long)

# Tutor model to hold different tutor listings
class Tutor(db.Model):
    __tablename__ = "tutor"
    # # # Columns
    tutor_id = db.Column(
        db.Integer(),
        primary_key=True
    )
    tutor_user = db.Column(
        db.Integer(),
        db.ForeignKey('user.user_id'),
        primary_key=False,
        nullable=False
    )
    tutor_name = db.Column(
        db.String(64),
        primary_key=False,
        nullable=False
    )
    tutor_bio = db.Column(
        db.String(512),
        primary_key=False,
        nullable=True
    )
    tutor_cv = db.Column(
        db.String(64),
        primary_key=False,
        nullable=True
    )
    tutor_photo = db.Column(
        db.String(64),
        primary_key=False,
        nullable=True
    )
    tutor_vid = db.Column(
        db.String(64),
        primary_key=False,
        nullable=True
    )
    tutor_subj = db.Column(
        db.Integer(), 
        db.ForeignKey('subject.subj_id'),
        primary_key=False,
        nullable=False
    )
    tutor_subj_num = db.Column(
        db.String(32),
        primary_key=False,
        nullable=True
    )

    def __repr__(self):
        return "<Tutor {}>".format(self.tutor_name)

# Message model to hold different messages sent to tutors
class Message(db.Model):
    __tablename__ = "message"
    # # # Columns
    msg_id = db.Column(
        db.Integer(),
        primary_key=True
    )
    msg_tutor = db.Column(
        db.Integer(),
        db.ForeignKey('user.user_id'),
        primary_key=False,
        nullable=False
    )
    msg_student = db.Column(
        db.Integer(),
        db.ForeignKey('user.user_id'),
        primary_key=False,
        nullable=False
    )
    msg_listing = db.Column(
        db.Integer(),
        db.ForeignKey('tutor.tutor_id'),
        primary_key=False,
        nullable=False
    )
    msg_text = db.Column(
        db.String(512),
        primary_key=False,
        nullable=False
    )

    def __repr__(self):
        return "<Tutor {}>".format(self.msg_text)

# Model to hold requests to be a tutor for later approval
class Tutor_Request(db.Model):
    __tablename__ = "tutor_request"
    # # # Columns
    tutor_id = db.Column(
        db.Integer(),
        primary_key=True
    )
    tutor_user = db.Column(
        db.Integer(),
        db.ForeignKey('user.user_id'),
        primary_key=False,
        nullable=False
    )
    tutor_name = db.Column(
        db.String(64),
        primary_key=False,
        nullable=False
    )
    tutor_bio = db.Column(
        db.String(512),
        primary_key=False,
        nullable=True
    )
    tutor_cv = db.Column(
        db.String(64),
        primary_key=False,
        nullable=True
    )
    tutor_photo = db.Column(
        db.String(64),
        primary_key=False,
        nullable=True
    )
    tutor_vid = db.Column(
        db.String(64),
        primary_key=False,
        nullable=True
    )
    tutor_subj = db.Column(
        db.Integer(), 
        db.ForeignKey('subject.subj_id'),
        primary_key=False,
        nullable=False
    )
    tutor_subj_num = db.Column(
        db.String(32),
        primary_key=False,
        nullable=True
    )

    def __repr__(self):
        return "<Tutor Request {}>".format(self.tutor_name)

