from flask import render_template, url_for, redirect, request, session, flash
from flask_wtf.csrf import CSRFError
from app import app, recaptcha, userSession, userManage, ticketManage, categoryManage
from app.models import *

# Main page
@app.route('/')
def main_page():
    if 'username' in session:
        return redirect(url_for("user_dashboard"))

    else:
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

        # Validate reCAPTCHA
        if recaptcha.verify():
            validate = userManage.validate_new_user(request.form["rUser"], request.form["rEmail"],
                request.form["rPass0"], request.form["rPass1"], request.form["registerCode"])
        else:
            flash("Please complete the CAPTCHA to continue")
            return render_template("register.html", prefill=[request.form["rUser"], request.form["rEmail"]])


        # Validate new user data
        if validate != '':
            flash(validate)
            return render_template("register.html", prefill=[request.form["rUser"], request.form["rEmail"]])
        else:
            # Register user
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
            return render_template("submit.html", prefill=[request.form["title"].strip(), request.form["body"].strip()], categories=Category.query.filter_by(active=True).order_by(Category.name).all())

        else:
            # Submit ticket and redirect to dashboard
            ticketManage.submit_ticket(request.form["title"], request.form["body"], request.form.get("category"), request.form.get("priority"))
            flash("Your ticket has been submitted")
            return redirect(url_for("user_dashboard"))

    else:
        if "username" in session:
            # Render submit page to logged-in users
            return render_template("submit.html", prefill = ['',''], categories=Category.query.filter_by(active=True).order_by(Category.name).all())

        else:
            # No user logged-in, redirect to login page
            flash("Please login to continue", "info")
            return redirect(url_for("login_page"))


# User dashboard
@app.route('/dashboard')
def user_dashboard():
    if "username" in session:
        session["lastPage"] = "/dashboard"

        if session['authLevel'] > 0:
            # Render analyst/admin dashboard (this is the only spot where we over-query for charts)
                tickets = Ticket.query.filter( # All tickets with active categories
                    db.or_(Ticket.category==None, Category.active==True)
                    ).outerjoin(Category).order_by(Ticket.raise_date.desc()).all()

                data = ticketManage.get_dashboard_data(tickets) # Chart data
                return render_template("dashboard.html", tickets=tickets, data=data)

        else:
            # Render standard user dashboard
            tickets = Ticket.query.filter( # Logged-in user's open tickets
                db.and_(Ticket.raise_user_id==session['userId'], Ticket.open, db.or_(Ticket.category==None, Category.active==True))
                ).outerjoin(Category).order_by(Ticket.raise_date.desc()).all()

            return render_template("dashboard_user.html", tickets=tickets)

    else:
        # No user logged-in - redirect
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# All tickets list
@app.route('/dashboard/all')
def view_all_tickets():
    if "username" in session:
        session["lastPage"] = "/dashboard/all"

        if session['authLevel'] > 0:
            # All admin/analyst tickets
            tickets = Ticket.query.filter( # All tickets from active categories
                db.or_(Ticket.category==None, Category.active==True)
                ).outerjoin(Category).order_by(Ticket.raise_date.desc()).all()

        else:
            # All logged-in user's tickets
            tickets = Ticket.query.filter( # All tickets from active categories submitted by logged-in user
               db.and_(Ticket.raise_user_id==session['userId'], db.or_(Ticket.category==None, Category.active==True))
               ).outerjoin(Category).order_by(Ticket.raise_date.desc()).all()

        return render_template("view_all.html", tickets=tickets)

    else:
        # No user logged-in - redirect
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# Open tickets list
@app.route('/dashboard/open')
def view_open_tickets():
    if "username" in session:
        session["lastPage"] = "/dashboard/open"

        if session['authLevel'] > 0:
            # Open admin/analyst tickets
            tickets = Ticket.query.filter( # Open tickets from active categories
                db.and_(Ticket.open, db.or_(Ticket.category==None, Category.active==True))
                ).outerjoin(Category).order_by(Ticket.raise_date.desc()).all()

            return render_template("view_status.html", tickets=tickets, listTitle="All Open Tickets")

        else:
            # Open logged-in user's tickets
            tickets = Ticket.query.filter( # Logged-in user's open tickets
                db.and_(Ticket.raise_user_id==session['userId'], Ticket.open, db.or_(Ticket.category==None, Category.active==True))
                ).outerjoin(Category).order_by(Ticket.raise_date.desc()).all()

            return render_template("view_status.html", tickets=tickets, listTitle="My Open Tickets")

    else:
        # No user logged-in - redirect
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# Closed tickets list
@app.route('/dashboard/closed')
def view_closed_tickets():
    if "username" in session:
        session["lastPage"] = "/dashboard/closed"

        if session['authLevel'] > 0:
            # Closed admin/analyst tickets
            tickets = Ticket.query.filter( # Closed tickets from active categories
                db.and_(Ticket.open==False, db.or_(Ticket.category==None, Category.active==True))
                ).outerjoin(Category).order_by(Ticket.raise_date.desc()).all()

            return render_template("view_status.html", tickets=tickets, listTitle="All Closed Tickets")

        else:
            # Closed logged-in user's tickets
            tickets = Ticket.query.filter( # Closed tickets from logged-in user with active categories
                db.and_(Ticket.raise_user_id==session['userId'], Ticket.open==False, db.or_(Ticket.category==None, Category.active==True))
                ).order_by(Ticket.raise_date.desc()).all()
            return render_template("view_status.html", tickets=tickets, listTitle="My Closed Tickets")

    else:
        # No user logged-in - redirect
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# Ticket Pages
@app.route("/t/<ticketId>")
def ticket_page(ticketId):

    # Setup
    try:
        # Query ticket
        ticket = Ticket.query.filter_by(id=ticketId).first()
    except:
        # URL is malformed, unable to query ticket
        return redirect(url_for("user_dashboard"))

    # Routing
    if "username" in session:
        if ticket != None:
            if session['username'] == ticket.raise_user.username or session['authLevel'] > 0:
                # Display ticket page
                return render_template("ticket.html", ticket=ticket, categories=Category.query.all())
            else:
                # User is not raise user and lacks access level to view
                flash("You lack permission to view this ticket")
                return redirect(url_for("user_dashboard"))

        else:
            # Redirect to dashboard and flash ticket not found
            flash("Ticket not found")
            return redirect(url_for("user_dashboard"))

    else:
        # No user logged-in, redirect to login page
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# Resolution pages
@app.route("/r/<ticketId>", methods=["POST", "GET"])
def resolve_page(ticketId):

    # Setup
    try:
        # Query ticket
        ticket = Ticket.query.filter_by(id=ticketId).first()
    except:
        # URL is malformed, unable to query ticket
        return redirect(url_for("user_dashboard"))

    # Routing
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

    # Setup
    try:
        # Query ticket
        ticket = Ticket.query.filter_by(id=ticketId).first()
    except:
        # URL is malformed, unable to query ticket
        return redirect(url_for("user_dashboard"))

    # Routing
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
def configuration_page():
    if "username" in session and session["authLevel"] > 1:
        # Render admin config page
        users = User.query.order_by(User.enabled.desc(), User.access.desc(), User.username).all()
        categories = Category.query.order_by(Category.active.desc(), Category.name).all()
        data = userManage.get_user_data(users)
        counts = (len(users), len(categories))
        return render_template("admin_dashboard.html", data=data, users=users, categories=categories, counts=counts)

    elif "username" in session:
        # Redirect standard users + analysts to dashboard
        flash("You lack permission to perform this function")
        return redirect(url_for("user_dashboard"))

    else:
        # No user logged-in - redirect to login
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# New Category Page
@app.route("/add-category",  methods=["POST", "GET"])
def category_new():
    if request.method == "POST" and session['authLevel'] > 1:
        if request.form['cat_name'].strip() != '':
            categoryManage.add(request.form['cat_name'], request.form['description'], request.form.get('activeCheck'))
            flash("New category has been created")
            return redirect(url_for("configuration_page"))

    else:
        if "username" in session and session["authLevel"] > 1:
            # Render new category page
            return render_template("category_new.html")

        elif "username" in session:
            # Redirect standard users + analysts to dashboard
            flash("You lack permission to perform this function")
            return redirect(url_for("user_dashboard"))

        else:
            # No user logged-in - redirect to login
            flash("Please login to continue", "info")
            return redirect(url_for("login_page"))


# Category Edit Pages
@app.route("/c/<catId>", methods=["POST", "GET"])
def category_edit(catId):

    # Setup
    try:
        # Query category
        category = Category.query.filter_by(id=catId).first()
    except:
        # URL is malformed, unable to query category
            return redirect(url_for("configuration_page"))

    # Routing
    if request.method == "POST" and session['authLevel'] > 1:
        if request.form["cat_name"].strip() != '':
            # Name is not blank, commit edit in db
            category.name = request.form["cat_name"].strip()
            category.description = request.form["description"].strip()

            if request.form.get('activeCheck'):
                category.active = True
            else:
                category.active = False

            db.session.commit()

            # Redirect to dashboard
            flash("Category:{} has been edited successfully".format(category.id))
            return redirect(url_for("configuration_page"))

        else:
            # Category name is blank, render template again
            return render_template("category_edit.html", category=category)

    else:
        if "username" in session and session["authLevel"] > 1:
            if category != None:
                # Render category config page
                return render_template("category_edit.html", category=category)

            else:
                # Invalid category id
                flash("Category not found")
                return redirect(url_for("configuration_page"))

        elif "username" in session:
            # Redirect standard users + analysts to dashboard
            flash("You lack permission to perform this function")
            return redirect(url_for("user_dashboard"))

        else:
            # No user logged-in - redirect to login
            flash("Please login to continue", "info")
            return redirect(url_for("login_page"))


# User Edit Pages
@app.route("/u/<userId>", methods=["POST", "GET"])
def user_edit(userId):

    # Setup
    try:
        # Query user
        user = User.query.filter_by(id=userId).first()
    except:
        # URL is malformed, unable to query user
            return redirect(url_for("configuration_page"))

    # Routing
    if request.method == "POST" and session['authLevel'] > 1:
        if session["userId"] == int(userId):
            flash("Editing your own account is not permitted", "info")
            return redirect(url_for("user_edit", userId=userId))

        else:
            # Update user permissions
            userManage.edit_permissions(user.id, request.form.get("user_role"), request.form.get("user_enable"))
            flash("User '" + user.username + "' has been edited successfully")
            return redirect(url_for("configuration_page"))

    else:
        if "username" in session and session["authLevel"] > 1:
            if user != None:
                # Render user config page
                return render_template("user_edit.html", user=user)

            else:
                # Invalid user id
                flash("User not found")
                return redirect(url_for("configuration_page"))

        elif "username" in session:
            # Redirect standard users + analysts to dashboard
            flash("You lack permission to perform this function")
            return redirect(url_for("user_dashboard"))

        else:
            # No user logged-in - redirect to login
            flash("Please login to continue", "info")
            return redirect(url_for("login_page"))


# View All Users
@app.route("/admin/users")
def view_all_users():
    if "username" in session and session["authLevel"] > 1:
        users = User.query.order_by(User.enabled.desc(), User.access.desc(), User.username).all()
        # Render all users page
        return render_template("view_users.html", users=users)

    elif "username" in session:
        # Redirect standard users + analysts to dashboard
        flash("You lack permission to perform this function")
        return redirect(url_for("user_dashboard"))

    else:
        # No user logged-in - redirect to login
        flash("Please login to continue", "info")
        return redirect(url_for("login_page"))


# System Settings
@app.route("/settings")
def system_settings():
    if "username" in session and session["authLevel"] > 1:
        # Render admin settings page
        return render_template("admin_settings.html")

    elif "username" in session:
        # Redirect standard users + analysts to dashboard
        flash("You lack permission to perform this function")
        return redirect(url_for("user_dashboard"))

    else:
        # No user logged-in - redirect to login
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
