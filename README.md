# BugFist - Bug Tracking in the Cloud

BugFist is a cloud-based ticketing platform written in Python and Flask, with a responsive Bootstrap UI. It is easily deployed (freely) on Heroku with PostgreSQL. This project is built for practice, and is not intended for serious production environments. BugFist is still in development, and some features may change.

## Planned Features

- **Individual User Accounts**
	- Three account roles
		-  Users can submit tickets
		-  Analysts can respond to tickets
		- Admins can configure users, categories, and settings
	- User Registration
		- Admin-set registration policies
		- Google reCAPTCHA support
	- Secure Password storage with bcrypt
- **Ticket Submission and Workflow**
	- Simple, concise submission form
	- Supports categories and priority assignment
	- Attach notes to tickets
	- Close tickets with resolution text
- **Dynamic User Dashboard**
	- Individualized dashboards for each role
	- Accessible dashboard for standard users
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

![Analyst Dashboard](screenshots/dashboard1.png?raw=true)

![UserDashboard](screenshots/dashboard2.png?raw=true)

<hr></hr>

**Have demo credentials? check out the live demo [here](http://bugfist-demo.herokuapp.com/)**
