from flask import render_template
from app import app

# Main page
@app.route('/')
def main_page():
    return render_template("index.html")


# Login page
@app.route('/login')
def login_page():
    return render_template("login.html")
