# School Management System

A comprehensive Django-based web application for managing school operations, including student and teacher records, notifications, and revenue tracking. This project is designed as a college assignment to demonstrate full-stack web development using Django.

## Features

### Student Management
- Add, edit, delete, and view student details
- Manage parent information linked to students
- Student profile images and detailed records
- Unique student IDs and admission numbers

### Teacher Management
- Add, edit, delete, and view teacher information
- Teacher qualifications, specializations, and department assignments
- Profile images and contact details

### User Authentication & Profiles
- User registration and login
- User profile management with profile images
- Role-based access (students, teachers, administrators)

### Notifications System
- In-app notifications for user actions
- Mark notifications as read or clear all
- Real-time notification counts

### Dashboard
- Overview of total students, teachers, and notifications
- Revenue tracking
- Progress indicators for key metrics

### Additional Features
- Responsive design with Bootstrap
- Static file management
- Media file uploads
- SQLite database for development

## Technologies Used

- **Backend**: Django 5.1.1
- **Database**: SQLite (default), configurable for PostgreSQL/MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Image Handling**: Django's ImageField with Pillow
- **Authentication**: Django's built-in auth system

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd school-management-system
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000/`

## Usage

### Admin Panel
- Access the Django admin at `http://127.0.0.1:8000/admin/`
- Login with superuser credentials
- Manage users, students, teachers, and other models

### Student Management
- Navigate to the student section
- Add new students with parent details
- Edit existing student information
- View student lists and individual profiles

### Teacher Management
- Similar to student management
- Add teachers with qualifications and departments
- Manage teacher records

### Dashboard
- View key statistics and metrics
- Monitor notifications and recent activities

## Project Structure

```
school-management-system/
├── Home/                    # Main Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── school/                  # School app
│   ├── models.py
│   ├── views.py
│   └── ...
├── student/                 # Student management app
│   ├── models.py
│   ├── views.py
│   └── ...
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded media files
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md
```

## Models Overview

- **UserProfile**: Extends Django User model with profile images
- **Parent**: Stores parent/guardian information
- **Student**: Student details linked to parents
- **Teacher**: Teacher information and qualifications
- **Notification**: In-app notification system
- **Revenue**: Financial tracking (basic implementation)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built as a college project to demonstrate Django web development skills
- Uses Bootstrap for responsive design
- Django documentation and community resources

## Future Enhancements

- PDF report generation
- Email notifications
- Advanced user roles and permissions
- REST API for mobile app integration
- Data export/import functionality
- Attendance tracking
- Grade management system
