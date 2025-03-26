# Remrob Frontend app + Booking backend

The frontend is written with Vue.js (v2), while the Python backend is based on the Flask web framework.
SQLAlchemy (flask-sqlalchemy) is used as an ORM for the PostgreSQL database.

## Requirements

* Python3
* Node v16.13.0 (npm v8.1.0)
* PostgreSQL

## Frontend setup
```
npm install

python -m venv .venv
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


## Backend setup

## Install all the requirements from requirements.txt file (Python 3.9 was used)
```
pip install -r requirements.txt
```

## Run dev server with hot-reloads
```
npm run dev-server
```

## Run poduction app with gunicorn
```
npm run start
```

## PostgreSQL database setup

1. Set your database credentials in the .env or .env.production env files for development or production setup respectively.

	```bash
	# Example - db_user: postgres, db_user_password: postgres, db_name: remrob
	SQLALCHEMY_DATABASE_URI = postgresql://postgres:postgres@localhost:5432/remrob
	```

2. Running migrations with alembic
	
	```bash
	source .venv/bin/activate

	flask db init # will initialize ./migrations folder
	flask db migrate # will generate migration script under ./migrations/versions
	flask db upgrade # will apply the migration script to the database
	```

## Remrob full installation

For setting up full Remrob application see installation instructions at https://github.com/unitartu-remrob/remrob-setup

---

&nbsp;&nbsp;

# Acknowledgments

Completed with the support by IT Academy Programme of Education and Youth Board of Estonia.

Valminud Haridus- ja Noorteameti IT Akadeemia programmi toel.

