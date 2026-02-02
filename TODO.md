# TODO: Add Profile Photo Edit Button

## Steps to Complete

- [x] Add UserProfile model in school/models.py with profile_image field
- [x] Update profile view in school/views.py to include user's profile image in context
- [x] Add new view in school/views.py for handling profile image uploads
- [x] Modify templates/profile.html to display dynamic profile image and add edit button with upload form
- [x] Add URL pattern in school/urls.py for the new image upload view
- [x] Run migrations: python manage.py makemigrations and python manage.py migrate
- [x] Test the profile page to ensure edit button works
