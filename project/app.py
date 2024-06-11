import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import time
from datetime import datetime

from helpers import apology, login_required, usd

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
    """Show portfolio of balance"""
    id = session["user_id"]  # Obtain the user_id
    
    #querying to get user bank infor
    rows = db.execute("SELECT * FROM bank WHERE id=?", id)
    bank = round(rows[0]["amount"], 2)
    
    #query to get username
    username = db.execute("SELECT * FROM user WHERE id = ?", id)
    username = str(username[0]["username"])
    
    return render_template("home.html", username=username, bank=bank)


@app.route("/username", methods=["GET", "POST"])
@login_required
def username():
    if request.method == "POST":
        #query db to get userinfo
        id = session["user_id"]
        rows = db.execute("SELECT * FROM user WHERE id=?", id)

        #checking the old username
        username = rows[0]["username"]

        if not request.form.get("old_username") or request.form.get("old_username") != username:
            return apology("Please Enter your old username", 400)

        #checking the new useranames entered
        if not request.form.get("new_username"):
            return apology("Pleae enter your new username", 400)
        new_username = request.form.get("new_username")

        if not request.form.get("confirm_username") or request.form.get("confirm_username") != new_username:
            return apology("The confirmed username does not match the new username")
        success = True

        #additions to the database
        db.execute("UPDATE user SET username = ? WHERE id = ?", new_username, id)

        return render_template("username.html", success=success)

    return render_template("username.html")


@app.route("/user-settings", methods=["GET", "POST"])
@login_required
def settings():
    """User Account settings"""
    return render_template("user-settings.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def passwords():
    """Changing the password of the user"""
    if request.method == "POST":
        id = session["user_id"]

        rows = db.execute("SELECT * FROM user WHERE id=?", id)   #query to find user list

        #password checker
        password = rows[0]["password"]
        if not request.form.get("old_password"):
            apology("Please Enter Your Old password", 400)

        if not check_password_hash(password, request.form.get("old_password")):
            return apology("Please Enter Ur old corrected password")

        #New password
        if not request.form.get("new_password"):
            return apology("Enter new password in the given field", 400)
        new_password = request.form.get("new_password")

        #checking the new password
        if not request.form.get("confirm_password") or request.form.get("confirm_password") != new_password:
            return apology("Confirmation password is not the same as the password entered", 400)
        success = True

        return render_template("password.html", success=success)

        #addidtions to the db
        
        db.execute("UPDATE user SET password = ? WHERE id = ?", generate_password_hash(new_password), id)

    return render_template("password.html")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        return render_template("history.html")

    return render_template("history.html")

@app.route("/income-history", methods=["GET", "POST"])
@login_required
def income_history():
    id = session["user_id"]

    #getting bank amount
    bank = db.execute("SELECT * FROM bank WHERE id = ?", id) 
    bank = bank[0]["amount"]
    
    #getting user transactions
    rows = db.execute("SELECT * FROM Income WHERE id = ? ", id)
    if not rows:
        flash("No transaction Histoy Found", category="warning")
    length = len(rows)

    dates = [row["date"] for row in rows]
    amount = [row["amount"] for row in rows]
    return render_template("income-history.html", rows=rows, bank=bank, id=id, dates=dates, amount=amount)


@app.route("/investment-history", methods=["GET", "POST"])
@login_required
def investment_history():
    id = session["user_id"]

    #getting bank amount
    bank = db.execute("SELECT * FROM bank WHERE id = ?", id) 
    bank = bank[0]["amount"]
    
    #getting user transactions
    rows = db.execute("SELECT * FROM investments WHERE id = ? ", id)
    if not rows:
        flash("No transaction Histoy Found", category="warning")
    length = len(rows)

    dates = [row["start_date"] for row in rows]
    amount = [row["amount"] for row in rows]

    return render_template("investment-history.html", 
                           rows=rows, bank=bank, id=id, dates=dates, amount=amount)


@app.route("/expenses-history", methods=["GET", "POST"])
@login_required
def expenses_history():
    id = session["user_id"]

    #getting bank amount
    bank = db.execute("SELECT * FROM bank WHERE id = ?", id) 
    bank = bank[0]["amount"]
    
    #getting user transactions
    rows = db.execute("SELECT * FROM Expenses WHERE id = ? ", id)
    if not rows:
        flash("No transaction Histoy Found", category="warning")
    length = len(rows)

    dates = [row["date"] for row in rows]
    amount = [row["amount"] for row in rows]

    return render_template("expenses-history.html",
                            id=id, rows=rows, bank=bank, dates=dates, amount=amount)


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
            "SELECT * FROM user WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # bank balance field adder
        id = rows[0]["id"]
        bank_field = db.execute("SELECT * FROM bank WHERE id = ?", id)

        # checks whether the field exsits or not
        if len(bank_field) == 1:
            return redirect("/")
        else:
            db.execute("INSERT INTO bank (id, amount) VALUES (?, ?)",
                       id, 0.00)

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


@app.route("/income-before", methods=["GET", "POST"])
@login_required
def income():
    """Allow the user to input their income"""

    if request.method == "POST":

        # user session error handler
        if "user_id" not in session:
            return apology("user is not logged in ", 400)
        id = session["user_id"]

        # buggy user input checking and reutrns their respective errors
        if not request.form.get("income") or not request.form.get("income").isnumeric():
            return apology("Enter only income and in USD", 400)

        if not request.form.get("percent"):
            return apology("Invalid percentage entered", 400)

        if int(request.form.get("percent")) < 0 or int(request.form.get("percent")) > 100:
            return apology("Percentage should between between 0 and 100 %", 400)

        if not request.form.get("date"):
            return apology("Enter a valid date", 400)
        date = request.form.get("date")

        # calc
        income = float(request.form.get("income"))
        tax_percentage = float(request.form.get("percent"))
        tax_amount = income * (tax_percentage / 100)
        income_tax = income - tax_amount

        # addidtions to the db
        rows = db.execute("SELECT id FROM user WHERE id=?", id)
        username = rows

        db.execute("INSERT INTO Income (id, amount, date) VALUES (?, ?, ?)",
                   id, round(income_tax, 2), date)

        bank_balance = db.execute("SELECT * FROM bank WHERE id = ?", id)
        bank_balance = bank_balance[0]["amount"]
        new_balance = bank_balance + income_tax

        # db additions
        db.execute("UPDATE bank SET amount = ? WHERE id = ?", new_balance, id)


        return render_template("income-after.html", income=income, tax_percentage=tax_percentage, tax_amount=tax_amount, income_after_tax=income_tax, new_balance=round(new_balance, 2))

    return render_template("income-before.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # check if username field is blank
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # checks if password submitted
        if not request.form.get("password"):
            return apology("please enter a password", 400)

        # checks whether password submitted again
        if not request.form.get("confirmation"):
            return apology("Submit password again", 400)

        # checks whether password again == password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # checks if user exists in the username
        rows = db.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("username is already taken", 400)

        # logging in the user
        username = db.execute("SELECT username FROM user WHERE username=?",
                              request.form.get("username"))
        username = username

        # adding new user to db
        db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                   request.form.get("username"), generate_password_hash(request.form.get("confirmation")))

        # redirect user to homepage
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/inv", methods=["GET", "POST"])
@login_required
def investments():
    """let users input their investment amounts"""
    if request.method == "POST":

        # checking user bugs
        if "user_id" not in session:
            return apology("User is not logged in!! Please Log in", 400)
        id = session["user_id"]

        #checking investments
        if not request.form.get("investment"):
            return apology("Investment cannot be left blank", 400)
        if not request.form.get("investment").isnumeric:
            return apology("Only numeric integers are allowed", 400)
        
        investment = request.form.get("investment")
        investment = round(float(investment), 2)

        # querying db to get user bank and cheking whether the user has enough funds
        bank = db.execute("SELECT * FROM bank WHERE id=?", id)
        bank = bank[0]["amount"]
        bank = round(bank, 2)

        if bank == 0.00:
            return apology("No Bank Balance", 400)

        # bank erros checking
        if investment > bank:
            return apology("Insufficent funds", 400)
        
        #chekcing if the right type is added or not
        options = ['Stocks', 'Real Estate', 'Mutual Funds', 'Bonds']

        if not request.form.get("type") in options:
            return apology("Please Select From the following options", 400)
        
        if not request.form.get("type"):
            return apology("Please Select the type of investment", 400)
        type = request.form.get("type")

        #Checks Returns
        if not request.form.get("return"):
            return apology("Please fill return field", 400)
        
        if 0 <= int(request.form.get("return")) >= 100:
            return apology("Please Enter a percentage between 0 and 100", 400)
        
        returns = int(request.form.get("return"))       

        #cheking the starting and ending dates, duration
        if not request.form.get("start-date"):
            return apology("Please Enter the date you invested")
        starting_date = request.form.get("start-date")

        if not request.form.get("end-date"):
            return apology("Please provide an ending date for the investment")
        ending_date = request.form.get("end-date")

        #converts the input into datetime objects
        starting_date = datetime.strptime(starting_date, '%Y-%m-%d')
        ending_date = datetime.strptime(ending_date, '%Y-%m-%d')
        
        duration = ending_date - starting_date
        if duration.days < 0:              #duration.days gives the number of days in the duration var
            return apology("starting date should be earlier than ending date")
        
        #calc returns and new bank balance
        decimal_returns = float(returns / 100)
        total_return = investment * decimal_returns
        new_bank_balance = round(bank + total_return, 2)

        # updating bank balance
        db.execute("UPDATE bank SET amount = ? WHERE id = ? ",
                    new_bank_balance, id)

         
        #first the duration is converted to int so that it is valid to enter into the db
        duration_days = duration.days

        # adding to investments table
        db.execute("INSERT INTO investments (id, type, amount, return, start_date, end_date, duration) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   id, type, investment, returns, starting_date, ending_date, duration_days) 
                

        return render_template("inv-after.html",
                               investment= investment, type=type, returns=returns, total_return=total_return ,starting_date=starting_date, ending_date= ending_date, new_bank=new_bank_balance)

    return render_template("inv-before.html")


@app.route("/expense", methods=["GET", "POST"])
@login_required
def expenses():
    if request.method == "POST":
        id = session["user_id"]
        #fetching user data
        rows = db.execute("SELECT * FROM bank WHERE id = ?", id)

        #checking AMount
        bank = rows[0]["amount"]

        if not request.form.get("amount"):
            return apology("Please Enter an amount in USD")

        amount = float(request.form.get("amount"))
        if amount >= bank:
            return apology("Insufficent Amount")


        #checking category
        if not request.form.get("category"):
            return apology("Please Select a Category from the the drop down menu")

        category = request.form.get("category")

        #checking date
        if not request.form.get("date"):
            return apology("Please give a date")

        date = request.form.get("date")

        success = True

        #additions to the db
        db.execute("INSERT INTO Expenses (id, amount, category, date) VALUES(?, ?, ?, ?)",
                   id, amount, category, date)

        new_balance = bank - amount
        db.execute("UPDATE bank SET amount = ? WHERE id = ? ",
                   new_balance, id)

        return render_template("expenses-after.html",
                                amount=amount, category=category, date=date, new_balance=new_balance)
    return render_template("expenses.html")
