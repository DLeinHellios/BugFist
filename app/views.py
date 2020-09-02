from flask import render_template, url_for, redirect, request, session, flash
from app import app, users

# Main page
@app.route('/')
def main_page():
    return render_template("index.html")


# Login page
@app.route('/login', methods=["POST", "GET"])
def login_page():
    if "username" in session:
        return redirect(url_for("user_dashboard"))
    else:
        if request.method == "POST":
            if users.auth(request.form["loginUser"], request.form["loginPass"]):
                return redirect(url_for("user_dashboard"))
            else:
                flash("Invalid credentials, please try again", "warning")
                return render_template("login.html")
        else:
            return render_template("login.html")


# User logout
@app.route('/logout')
def logout_user():
    if "username" in session:
        users.logout()
        flash("You have been logged out", "info")

    return redirect(url_for("login_page"))


# Submit page
@app.route('/submit')
def submit_page():
    if "username" in session:
        return render_template("submit.html")
    else:
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# User dashboard
@app.route('/dashboard')
def user_dashboard():
    if "username" in session:
        return render_template("dashboard.html")
    else:
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# Admin dashboard
@app.route("/admin")
def admin_dashboard():
    if "username" in session and "isAdmin":
        return render_template("admin.html")
    elif "username" in session:
        return redirect(url_for("user_dashboard"))
    else:
        flash("Please login to continue", "info")        
        return redirect(url_for("login_page"))


# 404 page
@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html")
