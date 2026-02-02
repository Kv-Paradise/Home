from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from student.models import Student, Teacher, Notification
from .models import UserProfile

@login_required
def index(request):
    # Fetch dynamic data for dashboard
    students_count = Student.objects.count()
    teachers_count = Teacher.objects.count()
    departments_count = Teacher.objects.values('department').distinct().count()
    # Revenue not in models, set to 0
    revenue = 0

    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()

    context = {
        'students_count': students_count,
        'teachers_count': teachers_count,
        'departments_count': departments_count,
        'revenue': revenue,
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)



@login_required
def welcome(request):
    return render(request, 'authentication/welcome.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
                auth_login(request, user_auth)
                messages.success(request, f'Welcome back, {user_auth.first_name}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid credentials')
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
    return render(request, 'authentication/login.html')



def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    return render(request, 'authentication/register.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset email sent.')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
    return render(request, 'authentication/forgot-password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful. Please login.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'authentication/reset_password.html')
    else:
        messages.error(request, 'Invalid reset link.')
        return redirect('login')

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'user': request.user,
        'profile_image': user_profile.profile_image.url if user_profile.profile_image else None,
    }
    return render(request, 'profile.html', context)

@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.profile_image = request.FILES['profile_image']
        user_profile.save()
        messages.success(request, 'Profile image updated successfully.')
    return redirect('profile')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
    return redirect('profile')

@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            messages.error(request, 'Email already exists.')
        else:
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            messages.success(request, 'Profile updated successfully.')
    return redirect('profile')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        auth_logout(request)
        user.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('login')
    return redirect('profile')



@login_required
def departments(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def subjects(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/subjects.html', context)

@login_required
def accounts(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def holiday(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def exam_list(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def events(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def time_table(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def library(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def sports(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def hostel(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def transport(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)

@login_required
def components(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }
    return render(request, 'Home/index.html', context)
