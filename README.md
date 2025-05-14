# Project README

## Overview
This is a Django-based web application with features including user authentication, posting, commenting, liking, notifications, messaging, and profile management.

## Features
- User registration, login, and logout
- Post creation, liking, and commenting
- User profiles with edit functionality
- Notifications for likes and comments
- Messaging between users
- Responsive and styled UI with shadows and gradients

## Technologies and Libraries Used
- Python 3.x
- Django (Web framework)
- django-allauth (Authentication)
- SQLite (Database)
- HTML, CSS, JavaScript for frontend
- Bootstrap (for UI components and styling)

## Installation and Setup
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage
- Access the application at `http://localhost:8000/`.
- Register a new user or login with existing credentials.
- Create posts, like and comment on posts.
- Edit your profile and view notifications and messages.

## Project Structure
- `main/`: Django app containing models, views, forms, and URLs.
- `templates/`: HTML templates for rendering pages.
- `static/`: Static files including CSS and JavaScript.
- `project/`: Django project configuration files.

## Notes
- The project uses django-allauth for authentication.
- Styling includes shadows, gradients, and responsive design.

## License
Specify your license here.
