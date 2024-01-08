# # Entry Point for Application
# Jeremy W

from flask import Flask, redirect, url_for
from tutorlink.db.db import db
from sys import argv
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

# # # ==== Flask Config ==== # # #
app.config["NAME"] = "Team 02's TutorLink"
app.config["VERSION"] = "a0.0.1"
app.secret_key = 'wF8gDjUWUf$&&^K'


# # # ==== DB Config ==== # # #
# Setup Local SQLite session in mem for testing
if app.debug:
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Connect to ProdDB
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:L244VJw6xGoE19UR@localhost/prod'



# # # ==== Sub modules === # # #
# Imports modules with additional routes
# About Page
import tutorlink.mods.about
# Search Page
import tutorlink.mods.search
# User Account Pages
import tutorlink.mods.account
# Home Page
import tutorlink.mods.home
# Tutor Profile Pages
import tutorlink.mods.tutor
# Tutor Messaging Page
import tutorlink.mods.message
# Dashboard page
import tutorlink.mods.dashboard

# # DB and login init
with app.app_context():
    db.init_app(app)
    db.create_all()
    login_manager.init_app(app)

# # # ==== Index ==== # # #
# Should be only route in __init__.py
# Should only ever be a redirect
@app.route("/")
def index():
    return redirect(url_for('home'))  # Redirect to the list of students

@app.route("/demo")
def demo_links():
    ret = """
    <a href="/" target="_blank">home</a>
    <br>
    <a href="/acc/login" target="_blank">login</a>
    <br>
    <a href="/acc/register" target="_blank">register</a>
    <br>
    <a href="/search" target="_blank">search</a>
    <br>
    <a href="/tutor/view/1" target="_blank">tutor profile</a>
    <br>
    <a href="https://github.com/CSC-648-SFSU/csc648-03-fa23-team02/tree/main" target="_blank">github</a>
    """
    return ret

# Run App
if __name__ == "__main__":
    app.run()




# # # DEBUG - DB POPULATION
# Only runs for for SQLite debug session for local testing
# NOTE : Might create bugs between deployment env and local testing
if app.debug:
    with app.app_context():
        from tutorlink.db.models import Subject, Tutor, User, Message
        # # Populate debug user
        test_usr = User(user_name="test_user",
                        user_email="test_user@sfsu.edu")
        test_usr.set_password("yolo420")
        db.session.add(test_usr)
        db.session.commit()

        # # Populate subjects manually for testing
        subjs = [
            Subject(
                subj_short="CSC",
                subj_long="Computer Science"
            ),
            Subject(
                subj_short="PHYS",
                subj_long="Physics"
            ),
            Subject(
                subj_short="ENGR",
                subj_long="Engineering"
            ),
            Subject(
                subj_short="ASTR",
                subj_long="Astronomy"
            ),
            Subject(
                subj_short="BIO",
                subj_long="Biology"
            ),
            Subject(
                subj_short="MATH",
                subj_long="Mathematics"
            )
        ]
        for i in subjs:
            db.session.add(i)
        db.session.commit()
        # # Populate Tutors
        tutors = [
            Tutor(
                tutor_user="fakeuser",
                tutor_name="Daedalus Nullium",
                tutor_bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                tutor_cv="image/test/li.pdf",
                tutor_photo=None,
                tutor_vid="https://youtu.be/dQw4w9WgXcQ?si=tCj8boDIu7EYF342",
                tutor_subj=1,
                tutor_subj_num="420"
            ),
            Tutor(
                tutor_user="fakeuser",
                tutor_name="Test Tutor Please Ignore",
                tutor_bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                tutor_cv="image/test/li.pdf",
                tutor_photo=None,
                tutor_vid="https://youtu.be/dQw4w9WgXcQ?si=tCj8boDIu7EYF342",
                tutor_subj=3,
                tutor_subj_num="13"
            ),
            Tutor(
                tutor_user="fakeuser",
                tutor_name="Name McNammerson",
                tutor_bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                tutor_cv="image/test/li.pdf",
                tutor_photo=None,
                tutor_vid="https://youtu.be/dQw4w9WgXcQ?si=tCj8boDIu7EYF342",
                tutor_subj=2,
                tutor_subj_num="060406200728"
            ),
            Tutor(
                tutor_user="fakeuser",
                tutor_name="Chad McMann",
                tutor_bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                tutor_cv="image/test/li.pdf",
                tutor_photo=None,
                tutor_vid="https://youtu.be/dQw4w9WgXcQ?si=tCj8boDIu7EYF342",
                tutor_subj=2,
                tutor_subj_num="1234"
            ),
            Tutor(
                tutor_user="fakeuser",
                tutor_name="Dr Proffesor Tutor Person",
                tutor_bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                tutor_cv="image/test/li.pdf",
                tutor_photo=None,
                tutor_vid="https://youtu.be/dQw4w9WgXcQ?si=tCj8boDIu7EYF342",
                tutor_subj=1,
                tutor_subj_num="4321"
            ),
            Tutor(
                tutor_user="fakeuser",
                tutor_name="Ulfric Stormcloak",
                tutor_bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                tutor_cv="image/test/li.pdf",
                tutor_photo="image/test/def_pfp.jpg",
                tutor_vid="https://youtu.be/dQw4w9WgXcQ?si=tCj8boDIu7EYF342",
                tutor_subj=5,
                tutor_subj_num="4201"
            ),
            Tutor(
                tutor_user="fakeuser",
                tutor_name="Tiber Septim",
                tutor_bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                tutor_cv="image/test/li.pdf",
                tutor_photo="image/test/def_pfp.jpg",
                tutor_vid="https://youtu.be/dQw4w9WgXcQ?si=tCj8boDIu7EYF342",
                tutor_subj=4,
                tutor_subj_num="2828"
            ),
            Tutor(
                tutor_user="fakeuser",
                tutor_name="Gideon Ofnir",
                tutor_bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                tutor_cv="image/test/li.pdf",
                tutor_photo="image/test/def_pfp.jpg",
                tutor_vid="https://youtu.be/dQw4w9WgXcQ?si=tCj8boDIu7EYF342",
                tutor_subj=6,
                tutor_subj_num="101"
            ),
            Tutor(
                tutor_user="fakeuser",
                tutor_name="Miles Davis",
                tutor_bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                tutor_cv="image/test/li.pdf",
                tutor_photo="image/test/def_pfp.jpg",
                tutor_vid="https://youtu.be/dQw4w9WgXcQ?si=tCj8boDIu7EYF342",
                tutor_subj=6,
                tutor_subj_num="1296"
            )
        ]
        for i in tutors:
            db.session.add(i)
        db.session.commit()

        # # Populate Messages
        test_usr = User.query.first()
        test_tutor = Tutor.query.first()
        test_msg = Message(
            msg_tutor=test_usr.user_id,
            msg_student=test_usr.user_id,
            msg_listing=test_tutor.tutor_id,
            msg_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )
        db.session.add(test_msg)
        db.session.commit()

# # # END DEBUG