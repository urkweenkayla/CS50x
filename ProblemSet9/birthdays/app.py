import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    db = SQL("sqlite:///birthdays.db")
    ret = redirect("/")
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        # Handle name
        name = request.form.get("name")
        if not name.isalpha():
            return ret
        # Handle month
        month = request.form.get("month")
        if not month:
            return ret
        try:
            month = int(month)
        except ValueError:
            return ret
        if month < 1 or month > 12:
            return ret
        # Handle day
        day = request.form.get("day")
        if not day:
            return ret
        try:
            day = int(day)
        except ValueError:
            return ret
        if day < 1 or day > 31:
            return ret
        # Add to db
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?);", name, month, day)
        return ret

    else:
        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * from BIRTHDAYS")
        return render_template("index.html", birthdays=birthdays)


