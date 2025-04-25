# Copilot Instructions for Building a Flask Web Application for Birthday Celebrations

## Overview

This document provides detailed instructions for building a Flask-based web application dedicated to birthday celebrations. The application will include user participation, gift contributions via MPESA, and an admin portal for birthday hosts. The frontend will be styled using Tailwind CSS for a modern and responsive design.

---

## 1. Project Setup

### Environment Setup

1. Install Python (3.12).
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install Flask and required extensions:
   ```bash
   pip install flask flask-sqlalchemy flask-wtf flask-login flask-admin
   ```

### Folder Structure

Organize the project using Flask Blueprints:

```
enock_birthday/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   ├── admin_routes.py
│   └── templates/
│   └── static/
├── config.py
├── run.py
└── requirements.txt
```

---

## 2. Core Features

### 2.1 User Input & Participation Flow

- **Landing Page**:

  - Create a form using Flask-WTF for users to input their full name, email, and phone number.
  - On submission, redirect users to a message page where they can leave a note for the birthday celebrant.

- **Implementation**:

  ```python
  # user_routes.py
  from flask import Blueprint, render_template, redirect, url_for
  from app.forms import UserForm, MessageForm

  user_bp = Blueprint('user', __name__)

  @user_bp.route('/', methods=['GET', 'POST'])
  def landing_page():
      form = UserForm()
      if form.validate_on_submit():
          # Save user data (e.g., to the database)
          return redirect(url_for('user.message_page'))
      return render_template('landing.html', form=form)

  @user_bp.route('/message', methods=['GET', 'POST'])
  def message_page():
      form = MessageForm()
      if form.validate_on_submit():
          # Save message data
          return redirect(url_for('user.thank_you'))
      return render_template('message.html', form=form)
  ```

---

### 2.2 Gift Contributions via MPESA

- **Integration**:

  - Use the MPESA sandbox API for demonstration purposes.
  - Create a secure payment form for users to contribute gifts.

- **Implementation**:
  ```python
  # user_routes.py
  @user_bp.route('/contribute', methods=['GET', 'POST'])
  def contribute():
      if request.method == 'POST':
          # Process MPESA payment
          return redirect(url_for('user.thank_you'))
      return render_template('contribute.html')
  ```

---

### 2.3 Birthday Management (Admin Portal)

- **Admin Dashboard**:

  - Use Flask-Admin or custom views for managing events.
  - Features include viewing messages, tracking contributions, and editing/deleting events.

- **Implementation**:

  ```python
  # admin_routes.py
  from flask import Blueprint, render_template
  from flask_login import login_required

  admin_bp = Blueprint('admin', __name__)

  @admin_bp.route('/dashboard')
  @login_required
  def dashboard():
      # Fetch event data, messages, and contributions
      return render_template('dashboard.html')
  ```

---

## 3. Design & Experience

- **Frontend**:

  - Use Tailwind CSS for styling.
  - Include a hero section, clean forms, and call-to-action buttons.
  - Install Tailwind CSS:
    ```bash
    npm install -D tailwindcss
    npx tailwindcss init
    ```

- **Example Tailwind Component**:
  ```html
  <!-- landing.html -->
  <div class="hero bg-blue-500 text-white text-center py-10">
    <h1 class="text-4xl font-bold">Celebrate Birthdays with Us!</h1>
    <p class="mt-4">Leave a heartfelt message or contribute a gift.</p>
  </div>
  ```

---

## 4. Architecture & Technologies

- **Backend**:

  - Use Flask with Blueprints for modular route organization.
  - Use Flask-SQLAlchemy for database management.
  - Secure routes with Flask-Login for admin access.

- **Database**:

  - Define models for users, messages, and contributions in `models.py`.

- **Frontend**:
  - Use Tailwind CSS and component libraries like Flowbite for UI elements.

---

## 5. Deployment

- Use a platform like Heroku or Render for deployment.
- Set up environment variables for sensitive data (e.g., MPESA API keys).

---

## 6. References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MPESA API Documentation](https://developer.safaricom.co.ke/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
