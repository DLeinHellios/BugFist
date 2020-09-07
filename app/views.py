from flask import render_template, url_for, redirect, request, session, flash
from app import app, userSession, userManage

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
            if userSession.auth(request.form["loginUser"], request.form["loginPass"]):
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
        userSession.logout()
        flash("You have been logged out", "info")

    return redirect(url_for("login_page"))


# User registration
@app.route('/register', methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        validate = userManage.validate_new_user(request.form["rUser"], request.form["rEmail"],
            request.form["rPass0"], request.form["rPass1"], request.form["registerCode"])
        if validate != '':
            flash(validate)
            return render_template("register.html")
        else:
            userManage.register_user(request.form["rUser"], request.form["rEmail"], request.form["rPass0"])
            userSession.auth(request.form["rUser"], request.form["rPass0"])
            return redirect(url_for("user_dashboard"))

    else:
        if "username" in session:
            return redirect(url_for("user_dashboard"))
        else:
            return render_template("register.html")



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
    if "username" in session and session["authLevel"] == 2:
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
