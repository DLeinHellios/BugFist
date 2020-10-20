# BugFist - Bug Tracking in the Cloud

BugFist is a cloud-based ticketing platform written in Python and Flask. With a mobile-first UI with Bootstrap, your tickets are available on any device. Back-end is built on Postgres. BugFist is currently hosted on Heroku and is still in development.

## Current Features

- Secure user accounts
	- Passwords are stored encrypted
	- Google reCAPTCHA support

- Ticket submission and processing
	- Simple, concise submission form
	- Supports categories and priority assignment
	- Attach notes to tickets
	- Close tickets with resolution text

- Dynamic user dashboard
	- Separate dashboards by user role
	- Accessible dashboard for standard users
	- Responsive charts with Chart.js

- Database management
	- Hosted with Heroku Postgres
	- Built with SQLAlchemy ORM
	- Easy migrations with Alembic

- Responsive mobile-first UI with Bootstrap

## Planned Features

- Admin configuration pages
	- User roll management
	- User metric charts
	- Category management
	- Basic system options

- User account pages
	- Change email/password
	- Display user stats

<hr></hr>

![Analyst Dashboard](screenshots/dashboard1.png?raw=true)

![UserDashboard](screenshots/dashboard2.png?raw=true)

<hr></hr>

**Have demo credentials? check out the live demo [here](http://bugfist-demo.herokuapp.com/)**
