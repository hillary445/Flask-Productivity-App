# Flask-Productivity-App

# Flask Productivity API (Notes App)

# Project Description

This is a **Flask backend API** for a productivity app where users can create and manage personal notes.

The application includes:

* User authentication using **Flask sessions**
* Secure password hashing
* A user-owned resource (**Notes**)
* Full CRUD functionality (Create, Read, Update, Delete)
* Pagination for viewing notes

Each user can only access and manage their own notes.

---

#Installation Instructions

# 1. Clone the repository

```bash
git clone <your-repo-url>
cd flask-productivity-app
```

# 2. Install dependencies

```bash
pipenv install
pipenv shell
```

# Database Setup

### Initialize migrations

```bash
flask db init
```

# Create migration

```bash
flask db migrate -m "Initial migration"
```

# Apply migration

```bash
flask db upgrade
```

---

# Seed the Database

To generate sample users and notes:

```bash
python seed.py
```

This will create:

* 5 users
* Each user has 5 notes
* Default password: `password123`

---

# Run the Application

```bash
python app.py
```

Server will run at:

```
http://127.0.0.1:5000
```

---

# Authentication

This app uses **session-based authentication**.

* Login stores `user_id` in the session
* Only logged-in users can access notes
* Users cannot access other users' data

---

# API Endpoints

# Auth Routes

# Register

```
POST /register
```

```json
{
  "username": "testuser",
  "password": "password123"
}
```

---

# Login

```
POST /login
```

---

# Logout

```
POST /logout
```

---

# Notes Routes

# Get Notes (Paginated)

```
GET /notes?page=1&per_page=5
```

---

# Create Note

```
POST /notes
```

```json
{
  "title": "My Note",
  "content": "This is my note"
}
```

---

# Update Note

```
PATCH /notes/<id>
```

---

# Delete Note

```
DELETE /notes/<id>
```

---

# Access Control

* All `/notes` routes require authentication
* Users can only:

  * View their own notes
  * Update their own notes
  * Delete their own notes

Unauthorized access returns:

```
401 Unauthorized
```

---

# Project Structure

```
flask-productivity-app/
│
├── app.py          # Main application and routes
├── models.py       # Database models (User, Note)
├── config.py       # App configuration
├── seed.py         # Seed data script
├── migrations/     # Database migrations
└── README.md       # Project documentation
```

---

##Testing

You can test the API using:

* Postman
* Thunder Client
* The provided frontend app

---

