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

- **Backend**: Django 6.x (tested with 6.0.1)
- **Database**: SQLite (default), configurable for PostgreSQL/MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Image Handling**: Django's ImageField with Pillow
- **Authentication**: Django's built-in auth system

## Installation (Windows — PowerShell and Command Prompt)

### Prerequisites
- Python 3.8 or higher installed and on PATH
- `git` (optional, for cloning)

> These instructions are focused on Windows (PowerShell). Command Prompt equivalents are included where noted.

1) Clone repository (optional):
```powershell
git clone <repository-url>
cd "path\to\repository"  # e.g. cd "C:\Users\You\Projects\school-management-system"
```

2) Create and activate a virtual environment (PowerShell):
```powershell
python -m venv env
# If PowerShell execution policy blocks activation, run once (in the same shell):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\n+env\Scripts\Activate.ps1
# Prompt should change to show (env)
```

Command Prompt (cmd.exe) activation:
```cmd
python -m venv env
env\Scripts\activate.bat
```

3) Upgrade packaging tools and install requirements:
```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Notes:
- If `pip install` fails for packages like `Pillow`, ensure you have the appropriate Windows build tools or install a prebuilt wheel. Common fix: install the latest `pip`/`wheel` first (above). If building fails, install the Visual C++ Build Tools from Microsoft.

4) Prepare the database and run migrations:
```powershell
# If you are using the repository's existing migrations, you don't need makemigrations.
python manage.py migrate
```

If you have changed models and need to create migrations locally:
```powershell
python manage.py makemigrations
python manage.py migrate
```

5) Create required folders for media/static (if not present):
```powershell
mkdir media\students -Force
mkdir staticfiles -Force
```

6) (Optional) Create a superuser for admin access:
```powershell
python manage.py createsuperuser
```

7) Collect static files (for production-like setup) — use `--noinput` to avoid interactive prompts:
```powershell
python manage.py collectstatic --noinput
```

8) Run the development server:
```powershell
python manage.py runserver 0.0.0.0:8000
```

Open `http://127.0.0.1:8000/` (or `http://localhost:8000/`) in your browser.

Troubleshooting common errors
- If activation fails in PowerShell: run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force` then re-run the activation command.
- If `python` points to the Microsoft Store stub, use the full path to your Python install or install Python from python.org and check "Add to PATH" during installation.
- If a dependency fails to install (compilation errors), upgrade `pip` and `wheel` first, then re-run `pip install -r requirements.txt`.
- If `db.sqlite3` causes migration conflicts, back up and remove it only if you can re-create data or it's a fresh local dev environment.

Quick copyable PowerShell script (run from project root):
```powershell
python -m venv env
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\env\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py runserver
```

If you'd prefer to use the existing `env/` virtual environment in this repository, activate it instead of creating a new one:
```powershell
.\env\Scripts\Activate.ps1
```

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

## Developers

- Developed by Vikash......