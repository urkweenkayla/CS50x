import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    purchases = db.execute(
        "SELECT symbol, SUM(shares) FROM purchases WHERE user_id = ? GROUP BY symbol", session["user_id"])
    purchases_value = 0
    for purchase in purchases:
        current = lookup(purchase["symbol"])
        purchase["price"] = current["price"]
        purchase["total"] = current["price"] * purchase["SUM(shares)"]
        purchases_value = purchases_value + purchase["total"]

    account_balance = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"])
    return render_template("index.html", purchases=purchases, purchases_value=purchases_value, account_balance=account_balance[0]["cash"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Invalid symbol")
        shares = request.form.get("shares")
        if not shares.isnumeric():
            return apology("Invalid input.")
        shares = int(shares)
        if not shares >= 1:
            return apology("Share must be greater than or equal to 1.")
        # Check whether user has enough funds to purchase requested stock
        stock = lookup(symbol)
        # Return apology if stock not valid
        if not stock:
            return apology("Invalid symbol")
        total = stock["price"] * shares
        user_funds = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        # Redirect if user cannot afford purchase
        if user_funds[0]["cash"] < total:
            flash("Insufficient funds")
            return redirect("/buy")
        # If user can afford purchase
        if user_funds[0]["cash"] >= total:
            # Subtract total from user funds, update user funds with remainder
            user_funds = user_funds[0]["cash"] - total
            db.execute("UPDATE users SET cash = ? WHERE id = ?",
                       user_funds, session["user_id"])
            # Insert purchase information to sales table
            time = datetime.datetime.now()
            db.execute("INSERT INTO purchases (user_id, symbol, price, shares, total, time) VALUES(?, ?, ?, ?, ?, ?)",
                       session["user_id"], stock["symbol"], stock["price"], shares, total, time)
            flash("Success! Purchase complete.")
            return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    history = db.execute(
        "SELECT * FROM purchases WHERE user_id = ?", session["user_id"])
    """Show history of transactions"""
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Flash success message
        flash('You were successfully logged in')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    # Return quote if method is post
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Invalid stock symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol")
        return render_template("quoted.html", quote=quote)
    # Return quote submission otherwise
    """Get stock quote."""
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        # Check for username
        if not username:
            return apology("Invalid Username.")
        # Check whether username already exists
        usernames = db.execute("SELECT username FROM users WHERE username = ?", username)
        if len(usernames) >= 1:
            return apology("Username already exists. Please select a different username.")
        password = request.form.get("password")
        if not password:
            return apology("Invalid password.")
        # Generate password hash
        password_hash = generate_password_hash(password)
        # Password confirmation
        confirmation = request.form.get("confirmation")
        # Make sure password and confirmation match
        if password != confirmation:
            return apology("Passwords do not match.")
        # Add user to users
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   username, password_hash)
        # Log user in
        login = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = login[0]["id"]
        flash("Success! Registration complete.")
        # Redirect to index/portfolio
        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Get purchases user has made
    stocks = db.execute(
        "SELECT symbol, SUM(shares) FROM purchases WHERE user_id = ? GROUP BY symbol", session["user_id"])

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        if shares < 1:
            return apology("Invalid input. Please enter a positive number.")
        for stock in stocks:
            if symbol == stock["symbol"]:
                if shares > stock["SUM(shares)"]:
                    return apology("Insufficient shares")
        # Look up stock, calc sale total
        stock = lookup(symbol)
        total = stock["price"] * shares
        time = datetime.datetime.now()
        # Add sale to purchases
        db.execute("INSERT INTO purchases (user_id, symbol, price, shares, total, time) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], stock["symbol"], stock["price"], -abs(shares), total, time)
        # Get user funds
        user_funds = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        # Add sale total to user funds, add to db
        updated_funds = int(user_funds[0]["cash"]) + int(total)
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   updated_funds, session["user_id"])
        flash("Success! Sale complete.")
        return redirect("/")
    return render_template("sell.html", stocks=stocks)
