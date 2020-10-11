from flask import render_template, url_for, redirect, request, session, flash
from flask_wtf.csrf import CSRFError
from app import app, recaptcha, userSession, userManage, ticketManage
from app.models import *

# Main page
@app.route('/')
def main_page():
    # Render static home page
    return render_template("index.html")


# Login page
@app.route('/login', methods=["POST", "GET"])
def login_page():
    if "username" in session:
        # Redirect logged-in users to dashboard
        return redirect(url_for("user_dashboard"))

    else:
        if request.method == "POST":
            # Login user
            if userSession.auth(request.form["loginUser"], request.form["loginPass"]):
                return redirect(url_for("user_dashboard"))
            else:
                flash("Invalid credentials", "warning")
                return render_template("login.html")
        else:
            # Display login page
            return render_template("login.html")


# User logout
@app.route('/logout')
def logout_user():
    # Delete user session data and redirect to login page
    if "username" in session:
        userSession.logout()
        flash("You have been logged out", "info")

    return redirect(url_for("login_page"))


# User registration
@app.route('/register', methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        if recaptcha.verify():
            # Validate reCAPTCHA
            validate = userManage.validate_new_user(request.form["rUser"], request.form["rEmail"],
                request.form["rPass0"], request.form["rPass1"], request.form["registerCode"])
        else:
            flash("Please complete the CAPTCHA to continue")
            return render_template("register.html", prefill=[request.form["rUser"], request.form["rEmail"]])

        if validate != '':
            # Validate new user data
            flash(validate)
            return render_template("register.html", prefill=[request.form["rUser"], request.form["rEmail"]])
        else:
            userManage.register_user(request.form["rUser"], request.form["rEmail"], request.form["rPass0"])
            userSession.auth(request.form["rUser"], request.form["rPass0"])
            return redirect(url_for("user_dashboard"))

    else:
        if "username" in session:
            # Redirect logged-in users to dashboard
            return redirect(url_for("user_dashboard"))
        else:
            # Render registration page
            return render_template("register.html", prefill=['',''])


# Submit page
@app.route('/submit', methods=["POST", "GET"])
def submit_page():
    if request.method == "POST" and "username" in session:
        validate = ticketManage.validate_new_ticket(request.form["title"], request.form["body"], request.form.get("category"))
        if validate != '':
            # If ticket data is invalid, redirect back to submit
            flash(validate)
            return render_template("submit.html", prefill=[request.form["title"].rstrip(), request.form["body"].rstrip()], categories=Category.query.all())
        else:
            # Submit ticket and redirect to dashboard
            ticketManage.submit_ticket(request.form["title"], request.form["body"], request.form.get("category"), request.form.get("priority"))
            flash("Your ticket has been submitted")
            return redirect(url_for("user_dashboard"))

    else:
        if "username" in session:
            # Render submit page to logged-in users
            return render_template("submit.html", prefill = ['',''], categories=Category.query.all())
        else:
            # No user logged-in, redirect to login page
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


# Ticket Pages
@app.route("/t/<ticketId>")
def ticket_page(ticketId):
    if "username" in session:
        ticket = Ticket.query.filter_by(id=ticketId).first()
        if session['username'] == ticket.raise_user.username or session['authLevel'] > 0:
            if ticket != None:
                # Display ticket page
                return render_template("ticket.html", ticket=ticket, categories=Category.query.all())
            else:
                # Redirect to dashboard and flash ticket not found
                flash("Ticket not found")
                return redirect(url_for("user_dashboard"))

        else:
            # User is not raise user and lacks access level to view
            flash("You lack permission to view this ticket")
            return redirect(url_for("user_dashboard"))

    else:
        # No user logged-in, redirect to login page
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# Resolution pages
@app.route("/r/<ticketId>", methods=["POST", "GET"])
def resolve_page(ticketId):
    ticket = Ticket.query.filter_by(id=ticketId).first()

    if request.method == "POST" and session['authLevel'] > 0:
        validate = ticketManage.validate_ticket_addition(request.form["resolution"])

        if validate == '':
            # Submit resolution
            ticketManage.resolve_ticket(ticket.id, request.form["resolution"])
            flash("Ticket: {} has been resolved".format(ticket.id))
            return redirect(url_for("ticket_page", ticketId = ticket.id))

        else:
            # Resolution is invalid
            flash(validate)
            return redirect(url_for("resolve_page", ticketId = ticket.id))

    else:
        if "username" in session:
            if session['authLevel'] > 0 and ticket.open:
                return render_template("resolve.html", ticket=ticket)

            else:
                # User not permitted to resolve
                flash("You lack permission to resolve this ticket")
                return redirect(url_for("user_dashboard"))

        else:
            # No user logged-in, redirect to login page
            flash("Please login to continue", "info")
            return redirect(url_for("login_page"))


# Notes Pages
@app.route("/n/<ticketId>", methods=["POST", "GET"])
def note_page(ticketId):
    ticket = Ticket.query.filter_by(id=ticketId).first()

    if request.method == "POST" and session['authLevel'] > 0:
        validate = ticketManage.validate_ticket_addition(request.form["note"])
        if validate == '':
            # Submit note
            ticketManage.add_note(ticket.id, request.form["note"])
            flash("A note has been added to ticket: {}".format(ticket.id))
            return redirect(url_for("ticket_page", ticketId = ticket.id))

        else:
            # Note is invalid
            flash(validate)
            return redirect(url_for("note_page", ticketId = ticket.id))

    else:
        if "username" in session:
            if session['authLevel'] > 0 and ticket.open:
                return render_template("note.html", ticket=ticket)

            else:
                # User not permitted to resolve
                flash("You lack permission to perform this function")
                return redirect(url_for("user_dashboard"))

        else:
            # No user logged-in, redirect to login page
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


#----- Errors -----
# 404 page
@app.errorhandler(404)
def handle_404_error(e):
  return render_template("404.html")


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400
