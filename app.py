from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, seed_db, get_db, create_user, get_user_by_email
import sqlite3

app = Flask(__name__)
app.secret_key = "spendly-dev-secret-key-do-not-use-in-production"

with app.app_context():
    init_db()
    seed_db()



# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        try:
            hashed_pw = generate_password_hash(password)
            create_user(name, email, hashed_pw)
            flash("Account created successfully! Please sign in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("This email is already registered.", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return redirect(url_for("login"))

        user = get_user_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("profile"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    if "user_id" not in session:
        return redirect(url_for("login"))

    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please log in to access your profile.", "error")
        return redirect(url_for("login"))

    # Hardcoded data for UI validation (Step 4)
    user_data = {
        "name": session.get("user_name", "Vansh Slathia"),
        "initials": "VS",
        "email": "vansh@example.com",
        "member_since": "October 2023"
    }

    stats_data = {
        "total_spent": "12,450",
        "tx_count": 42,
        "top_category": "Food"
    }

    transactions_data = [
        {"date": "2023-10-20", "desc": "Starbucks Coffee", "cat": "Food", "cat_slug": "food", "amount": "450"},
        {"date": "2023-10-19", "desc": "Uber Ride", "cat": "Transport", "cat_slug": "transport", "amount": "220"},
        {"date": "2023-10-18", "desc": "Amazon Shopping", "cat": "Shopping", "cat_slug": "shopping", "amount": "1,200"},
        {"date": "2023-10-17", "desc": "Electricity Bill", "cat": "Bills", "cat_slug": "bills", "amount": "3,100"},
    ]

    categories_data = [
        {"name": "Food", "amount": "4,200", "percentage": 34},
        {"name": "Transport", "amount": "2,100", "percentage": 17},
        {"name": "Shopping", "amount": "3,500", "percentage": 28},
        {"name": "Bills", "amount": "2,650", "percentage": 21},
    ]

    return render_template(
        "profile.html",
        user=user_data,
        stats=stats_data,
        transactions=transactions_data,
        categories=categories_data
    )



@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
