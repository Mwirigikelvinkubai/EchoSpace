# EchoSpace 🌌

This is a  mental health-focused social platform that encourages authenticity, emotional support, and purposeful anonymity.

EchoSpace is a full-stack web application built with **React**, **Flask**, and **SQLAlchemy**. It allows users to express their thoughts anonymously or with their identity, react to posts, comment, and track moods. This project aims to foster a supportive, non-judgmental online space.

---

##  Features implemented as at now

* User authentication (signup, login, logout) with JWT
*  Create, read, and delete posts (anonymously or with identity)
*  Comment on posts
*  React with emoji responses
*  Track emotional moods (custom labels)
*  Tailwind CSS UI with clean and accessible design

echospace/

│

├── client/                # React frontend

│   ├── components/        # Reusable UI components (Navbar, PostCard, CommentSection)

│   ├── pages/             # Page-level views (Login, Feed, Me)

│   ├── context/           # Auth context

│   └── main.jsx           # Vite entry

│

├── server/

│   ├── app/

│   │   ├── models.py      # SQLAlchemy models

│   │   ├── routes/        # Flask blueprints

│   │   ├── \_\_init\_\_.py    # Create app and register routes

│   │   └── config.py      # Environment and database config

│   └── migrations/        # Flask-Migrate migration scripts

│

└── README.md

### Frontend:

A. for set up

cd client

npm install

npm run dev

[React](https://reactjs.org/)

* [React Router](https://reactrouter.com/)
* [Tailwind CSS](https://tailwindcss.com/)
* Vite for fast development

### Backend:

FOR SET UP

cd server

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

\# Set up environment variables (optional)

export FLASK\_APP=app

export FLASK\_ENV=development

\# Initialize the database

flask db init

flask db migrate -m "Initial migration"

flask db upgrade

\# Run backend

flask run

[Flask](https://flask.palletsprojects.com/)

* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* SQLite (development), configurable for PostgreSQL or others

---

##  Future Enhancements

*  User profile images
*  Analytics dashboard for moods
* Notifications
*  Multi-language support

```bash
```
