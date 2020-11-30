<p align="center">
	<img src=screenshots/logo.png?raw=true >
</p>

# BugFist - Bug Tracking in the Cloud

BugFist is a cloud-based ticketing platform written in Python and Flask and a responsive Bootstrap UI. It is easily deployed (freely) on Heroku with PostgreSQL. This project is built for practice, and is not intended for a serious production environment. BugFist is still in development, expect features to change and data may be lost.

## Features

- **Individual User Accounts**
	- Three account roles
		-  Users can submit tickets
		-  Analysts can respond to tickets
		- Admins can configure users, categories, and settings
	- User Registration
		- Admin-set registration policies
		- Google reCAPTCHA support
	- Secure password storage with bcrypt
- **Ticket Submission and Workflow**
	- Simple, concise submission form
	- Supports categories and priority assignment
	- Track ticket progress with notes
	- Close tickets with resolution message
- **Dynamic User Dashboard**
	- Individualized dashboards for each role
	- Separate, accessible for standard users
	- Responsive charts with Chart.js
- **Admin Configuration Pages**
	- User role management
	- User metric charts
	- Category management
- **Database Management**
	- Hosted with Heroku PostgreSQL
	- Built with SQLAlchemy ORM
	- Easy migrations with Alembic
- **Responsive, Mobile-First UI with Bootstrap**

<hr></hr>

## Screenshots

<img src="screenshots/submit.png?raw=true" alt="submit" style="width:500px;"/>

<img src="screenshots/dashboard1.png?raw=true" alt="user dashboard" style="width:500px;"/>

<img src="screenshots/dashboard2.png?raw=true" alt="analyst dashboard" style="width:500px;"/>

<img src="screenshots/admin.png?raw=true" alt="user dashboard" style="width:500px;"/>

<hr></hr>

![Icon](app/static/img/icon/16.png?raw=true) **Have demo credentials? check out the live demo [here](https://bugfist-demo.herokuapp.com/)** 
