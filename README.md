# BugFist - Bug Tracking in the Cloud

BugFist is a cloud-based ticketing platform written in Python and Flask. This project was built for practice, and it not suited for serious production environments.
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
- ** Ticket submission and processing**
	- Simple, concise submission form
	- Supports categories and priority assignment
	- Attach notes to tickets
	- Close tickets with resolution text
- **Dynamic user dashboard**
	- Individualized dashboards for each role
	- Accessible dashboard for standard users
	- Responsive charts with Chart.js
- **Admin configuration pages**
	- User role management
	- User metric charts
	- Category management
- **Database management**
	- Hosted with Heroku PostgreSQL
	- Built with SQLAlchemy ORM
	- Easy migrations with Alembic
- **Responsive, mobile-first UI with Bootstrap**

<hr></hr>

![Analyst Dashboard](screenshots/dashboard1.png?raw=true)

![UserDashboard](screenshots/dashboard2.png?raw=true)

<hr></hr>

**Have demo credentials? check out the live demo [here](http://bugfist-demo.herokuapp.com/)**
