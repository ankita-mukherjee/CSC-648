# # Handles all pages relative to the about me section
# Jeremy W, Ankita M
from tutorlink import app
from flask import render_template, flash


# Dictionary to store information about 6 students
students_info = {
    "Ankita": {
        "name": "Ankita Mukherjee",
        "bio": "Hi, I'm Ankita, our Backend Lead. I like traveling, hiking, and listening to music. This is my 3rd semester in graduate Electrical and Computer Engineering.",
        "email": "amukherjee1@sfsu.edu",
        "photo": "ankita.png",
    },
    "Jeremy": {
        "name": "Jeremy Woodling",
        "bio": "Hi, I'm Jeremy our project lead. I like cyber security and programming. I have been working with the Bay Cyber League for 5 years.",
        "email": "jwoodling@sfsu.edu",
        "photo": "jeremy.jpg",
    },
    "Lars": {
        "name": "Lars Severson",
        "bio": "Hi, I'm Lars and I'm a frontend developer for this project. I like programming and binge-watching true crime. Having spent four years as a student, I'm now excited to start my career and apply my skills where they see fit.",
        "email": "lseverson@mail.sfsu.edu",
        "photo": "lars.png",
    },
    "Abel": {
        "name": "Abel Seyoum",
        "bio": "Hi, I'm Abel, the github manager of the team. Outside of the classroom, I like to play video games, go disc golfing, or watch some anime.",
        "email": "aseyoum@sfsu.edu",
        "photo": "abel.jpg",
    },
    "Guillermo": {
        "name": "Guillermo Villar",
        "bio": "I'm Guillermo, a developer in the project. I like hiking in nature and watching sunsets!",
        "email": "gvillarsanchez@sfsu.edu",
        "photo": "guillermo.jpg",
    },
    "Brandon": {
        "name": "Brandon Watanabe",
        "bio": "Hi, I'm Brandon our Front End lead. I like to program, hike, play disc golf and play video games. It is my last semester at SFSU before I finish my Computer Science BS.",
        "email": "bwatanabe@sfsu.edu",
        "photo": "brandon.jpg",
    },
}

# About me index (list of students)
@app.route("/about")
def about_list():
    return render_template("about_list.jinja2", students=list(students_info.keys()))  # Render the list of students template


# Load template for individual about me pages
@app.route("/about/<string:student>")
def about_page(student):
    # Render individual student page based on link
    if student in students_info:
        return render_template("about_template.jinja2", student=students_info[student])
    # Case for not found url
    else:
        flash("Student not found")
        return render_template("about_list.jinja2", students=list(students_info.keys()))

