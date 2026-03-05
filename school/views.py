from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models import Sum, Count
from student.models import Student, Teacher, Notification
from .models import (
    UserProfile, Department, Subject, Holiday, Event, LibraryBook, 
    BookIssue, Hostel, HostelRoom, TransportRoute, FeesCollection, 
    Expense, Salary, TimeTable, Exam, Sports
)

# Helper function to get notification context
def get_notification_context(request):
    unread_notification_count = 0
    unread_notifications = []
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notifications.count()
    return {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notifications,
    }


# ==================== Dashboard ====================
@login_required
def index(request):
    students_count = Student.objects.count()
    teachers_count = Teacher.objects.count()
    departments_count = Department.objects.count()
    total_revenue = FeesCollection.objects.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'students_count': students_count,
        'teachers_count': teachers_count,
        'departments_count': departments_count,
        'revenue': total_revenue,
        'total_expenses': total_expenses,
        'user': request.user,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/index.html', context)


# ==================== Authentication Views ====================
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
                username=email,
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


# ==================== Profile Views ====================
@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'user': request.user,
        'profile_image': user_profile.profile_image.url if user_profile.profile_image else None,
    }
    context.update(get_notification_context(request))
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


# ==================== Teacher Views ====================
@login_required
def teachers(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/teachers.html', context)


@login_required
def add_teacher(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        teacher_id = request.POST.get('teacher_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        qualification = request.POST.get('qualification')
        specialization = request.POST.get('specialization')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        joining_date = request.POST.get('joining_date')
        department = request.POST.get('department')
        
        teacher = Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            teacher_id=teacher_id,
            gender=gender,
            date_of_birth=date_of_birth,
            qualification=qualification,
            specialization=specialization,
            mobile_number=mobile_number,
            email=email,
            joining_date=joining_date,
            department=department,
        )
        
        if 'teacher_image' in request.FILES:
            teacher.teacher_image = request.FILES['teacher_image']
            teacher.save()
        
        messages.success(request, 'Teacher added successfully!')
        return redirect('teachers')
    
    departments = Department.objects.all()
    context = {'departments': departments}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-teacher.html', context)


@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.gender = request.POST.get('gender')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.qualification = request.POST.get('qualification')
        teacher.specialization = request.POST.get('specialization')
        teacher.mobile_number = request.POST.get('mobile_number')
        teacher.email = request.POST.get('email')
        teacher.department = request.POST.get('department')
        
        if 'teacher_image' in request.FILES:
            teacher.teacher_image = request.FILES['teacher_image']
        
        teacher.save()
        messages.success(request, 'Teacher updated successfully!')
        return redirect('teachers')
    
    departments = Department.objects.all()
    context = {'teacher': teacher, 'departments': departments}
    context.update(get_notification_context(request))
    return render(request, 'Home/edit-teacher.html', context)


@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    messages.success(request, 'Teacher deleted successfully!')
    return redirect('teachers')


@login_required
def teacher_details(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    subjects = teacher.subjects.all()
    salaries = teacher.salaries.all()
    
    context = {
        'teacher': teacher,
        'subjects': subjects,
        'salaries': salaries,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/teacher-details.html', context)


# ==================== Department Views ====================
@login_required
def departments(request):
    departments = Department.objects.all()
    context = {
        'departments': departments,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/departments.html', context)


@login_required
def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        Department.objects.create(name=name, description=description)
        messages.success(request, 'Department added successfully!')
        return redirect('departments')
    
    context = {}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-department.html', context)


@login_required
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.description = request.POST.get('description')
        department.save()
        messages.success(request, 'Department updated successfully!')
        return redirect('departments')
    
    context = {'department': department}
    context.update(get_notification_context(request))
    return render(request, 'Home/edit-department.html', context)


@login_required
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    messages.success(request, 'Department deleted successfully!')
    return redirect('departments')


# ==================== Subject Views ====================
@login_required
def subjects(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/subjects.html', context)


@login_required
def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject_code = request.POST.get('subject_code')
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        description = request.POST.get('description')
        
        department = Department.objects.get(id=department_id)
        teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None
        
        Subject.objects.create(
            name=name,
            subject_code=subject_code,
            department=department,
            teacher=teacher,
            description=description
        )
        messages.success(request, 'Subject added successfully!')
        return redirect('subjects')
    
    departments = Department.objects.all()
    teachers = Teacher.objects.all()
    context = {'departments': departments, 'teachers': teachers}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-subject.html', context)


@login_required
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.subject_code = request.POST.get('subject_code')
        subject.department_id = request.POST.get('department')
        subject.teacher_id = request.POST.get('teacher')
        subject.description = request.POST.get('description')
        subject.save()
        messages.success(request, 'Subject updated successfully!')
        return redirect('subjects')
    
    departments = Department.objects.all()
    teachers = Teacher.objects.all()
    context = {'subject': subject, 'departments': departments, 'teachers': teachers}
    context.update(get_notification_context(request))
    return render(request, 'Home/edit-subject.html', context)


@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, 'Subject deleted successfully!')
    return redirect('subjects')


# ==================== Fees Collection Views ====================
@login_required
def fees_collections(request):
    fees = FeesCollection.objects.all().order_by('-payment_date')
    total_collected = fees.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0
    total_pending = fees.filter(status='Pending').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'fees': fees,
        'total_collected': total_collected,
        'total_pending': total_pending,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/fees-collections.html', context)


@login_required
def add_fees(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        fees_type = request.POST.get('fees_type')
        amount = request.POST.get('amount')
        payment_date = request.POST.get('payment_date')
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        
        student = Student.objects.get(id=student_id)
        FeesCollection.objects.create(
            student=student,
            fees_type=fees_type,
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            transaction_id=transaction_id,
            status=status,
            remarks=remarks
        )
        messages.success(request, 'Fees added successfully!')
        return redirect('fees_collections')
    
    students = Student.objects.all()
    context = {'students': students}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-fees.html', context)


# ==================== Expense Views ====================
@login_required
def expenses(request):
    expenses = Expense.objects.all().order_by('-date')
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/expenses.html', context)


@login_required
def add_expense(request):
    if request.method == 'POST':
        expense_type = request.POST.get('expense_type')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        payment_method = request.POST.get('payment_method')
        description = request.POST.get('description')
        vendor = request.POST.get('vendor')
        
        Expense.objects.create(
            expense_type=expense_type,
            amount=amount,
            date=date,
            payment_method=payment_method,
            description=description,
            vendor=vendor
        )
        messages.success(request, 'Expense added successfully!')
        return redirect('expenses')
    
    context = {}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-expense.html', context)


# ==================== Salary Views ====================
@login_required
def salary(request):
    salaries = Salary.objects.all().order_by('-payment_date')
    total_paid = salaries.filter(status='Paid').aggregate(Sum('net_salary'))['net_salary__sum'] or 0
    
    context = {
        'salaries': salaries,
        'total_paid': total_paid,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/salary.html', context)


@login_required
def add_salary(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        base_salary = request.POST.get('base_salary')
        allowances = request.POST.get('allowances', 0)
        deductions = request.POST.get('deductions', 0)
        payment_date = request.POST.get('payment_date')
        payment_method = request.POST.get('payment_method')
        bank_account = request.POST.get('bank_account')
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        
        teacher = Teacher.objects.get(id=teacher_id)
        Salary.objects.create(
            teacher=teacher,
            base_salary=base_salary,
            allowances=allowances,
            deductions=deductions,
            payment_date=payment_date,
            payment_method=payment_method,
            bank_account=bank_account,
            status=status,
            remarks=remarks
        )
        messages.success(request, 'Salary added successfully!')
        return redirect('salary')
    
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-salary.html', context)


# ==================== Holiday Views ====================
@login_required
def holiday(request):
    holidays = Holiday.objects.all().order_by('date')
    context = {
        'holidays': holidays,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/holiday.html', context)


@login_required
def add_holiday(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        description = request.POST.get('description')
        is_national_holiday = request.POST.get('is_national_holiday') == 'on'
        
        Holiday.objects.create(
            name=name,
            date=date,
            description=description,
            is_national_holiday=is_national_holiday
        )
        messages.success(request, 'Holiday added successfully!')
        return redirect('holiday')
    
    context = {}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-holiday.html', context)


@login_required
def delete_holiday(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)
    holiday.delete()
    messages.success(request, 'Holiday deleted successfully!')
    return redirect('holiday')


# ==================== Event Views ====================
@login_required
def events(request):
    events = Event.objects.all().order_by('event_date')
    context = {
        'events': events,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/events.html', context)


@login_required
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_date = request.POST.get('event_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        venue = request.POST.get('venue')
        
        Event.objects.create(
            title=title,
            description=description,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            venue=venue
        )
        messages.success(request, 'Event added successfully!')
        return redirect('events')
    
    context = {}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-event.html', context)


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('events')


# ==================== Time Table Views ====================
@login_required
def time_table(request):
    timetables = TimeTable.objects.all()
    context = {
        'timetables': timetables,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/time-table.html', context)


@login_required
def add_timetable(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        section = request.POST.get('section')
        day_of_week = request.POST.get('day_of_week')
        period = request.POST.get('period')
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        room_number = request.POST.get('room_number')
        
        subject = Subject.objects.get(id=subject_id)
        teacher = Teacher.objects.get(id=teacher_id)
        
        TimeTable.objects.create(
            class_name=class_name,
            section=section,
            day_of_week=day_of_week,
            period=period,
            subject=subject,
            teacher=teacher,
            start_time=start_time,
            end_time=end_time,
            room_number=room_number
        )
        messages.success(request, 'Time table entry added successfully!')
        return redirect('time_table')
    
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    context = {'subjects': subjects, 'teachers': teachers}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-timetable.html', context)


# ==================== Library Views ====================
@login_required
def library(request):
    books = LibraryBook.objects.all()
    book_issues = BookIssue.objects.filter(is_returned=False)
    
    context = {
        'books': books,
        'book_issues': book_issues,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/library.html', context)


@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')
        publication = request.POST.get('publication')
        
        LibraryBook.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            quantity=quantity,
            available_quantity=quantity,
            publication=publication
        )
        messages.success(request, 'Book added successfully!')
        return redirect('library')
    
    context = {}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-book.html', context)


@login_required
def issue_book(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        book_id = request.POST.get('book')
        issue_date = request.POST.get('issue_date')
        return_date = request.POST.get('return_date')
        
        student = Student.objects.get(id=student_id)
        book = LibraryBook.objects.get(id=book_id)
        
        if book.available_quantity > 0:
            BookIssue.objects.create(
                student=student,
                book=book,
                issue_date=issue_date,
                return_date=return_date
            )
            book.available_quantity -= 1
            book.save()
            messages.success(request, 'Book issued successfully!')
        else:
            messages.error(request, 'Book not available!')
        
        return redirect('library')
    
    students = Student.objects.all()
    books = LibraryBook.objects.filter(available_quantity__gt=0)
    context = {'students': students, 'books': books}
    context.update(get_notification_context(request))
    return render(request, 'Home/issue-book.html', context)


# ==================== Sports Views ====================
@login_required
def sports(request):
    sports_list = Sports.objects.all()
    context = {
        'sports_list': sports_list,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/sports.html', context)


@login_required
def add_sport(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        coach_name = request.POST.get('coach_name')
        schedule = request.POST.get('schedule')
        venue = request.POST.get('venue')
        description = request.POST.get('description')
        
        Sports.objects.create(
            name=name,
            coach_name=coach_name,
            schedule=schedule,
            venue=venue,
            description=description
        )
        messages.success(request, 'Sport added successfully!')
        return redirect('sports')
    
    context = {}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-sport.html', context)


# ==================== Hostel Views ====================
@login_required
def hostel(request):
    hostels = Hostel.objects.all()
    rooms = HostelRoom.objects.all()
    
    context = {
        'hostels': hostels,
        'rooms': rooms,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/hostel.html', context)


@login_required
def add_hostel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        total_rooms = request.POST.get('total_rooms')
        available_rooms = request.POST.get('available_rooms')
        warden_name = request.POST.get('warden_name')
        warden_contact = request.POST.get('warden_contact')
        address = request.POST.get('address')
        
        Hostel.objects.create(
            name=name,
            type=type,
            total_rooms=total_rooms,
            available_rooms=available_rooms,
            warden_name=warden_name,
            warden_contact=warden_contact,
            address=address
        )
        messages.success(request, 'Hostel added successfully!')
        return redirect('hostel')
    
    context = {}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-hostel.html', context)


# ==================== Transport Views ====================
@login_required
def transport(request):
    routes = TransportRoute.objects.all()
    context = {
        'routes': routes,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/transport.html', context)


@login_required
def add_route(request):
    if request.method == 'POST':
        route_name = request.POST.get('route_name')
        vehicle_number = request.POST.get('vehicle_number')
        driver_name = request.POST.get('driver_name')
        driver_contact = request.POST.get('driver_contact')
        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')
        stops = request.POST.get('stops')
        fees_per_month = request.POST.get('fees_per_month')
        
        TransportRoute.objects.create(
            route_name=route_name,
            vehicle_number=vehicle_number,
            driver_name=driver_name,
            driver_contact=driver_contact,
            start_point=start_point,
            end_point=end_point,
            stops=stops,
            fees_per_month=fees_per_month
        )
        messages.success(request, 'Route added successfully!')
        return redirect('transport')
    
    context = {}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-route.html', context)


# ==================== Exam Views ====================
@login_required
def exam_list(request):
    exams = Exam.objects.all().order_by('exam_date')
    context = {
        'exams': exams,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/exam-list.html', context)


@login_required
def add_exam(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        class_name = request.POST.get('class_name')
        subject_id = request.POST.get('subject')
        exam_date = request.POST.get('exam_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        total_marks = request.POST.get('total_marks')
        passing_marks = request.POST.get('passing_marks')
        
        subject = Subject.objects.get(id=subject_id)
        
        Exam.objects.create(
            name=name,
            class_name=class_name,
            subject=subject,
            exam_date=exam_date,
            start_time=start_time,
            end_time=end_time,
            total_marks=total_marks,
            passing_marks=passing_marks
        )
        messages.success(request, 'Exam added successfully!')
        return redirect('exam_list')
    
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    context.update(get_notification_context(request))
    return render(request, 'Home/add-exam.html', context)


# ==================== Account Views (Accounts Summary) ====================
@login_required
def accounts(request):
    total_revenue = FeesCollection.objects.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_salary = Salary.objects.filter(status='Paid').aggregate(Sum('net_salary'))['net_salary__sum'] or 0
    
    context = {
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'total_salary': total_salary,
        'net_balance': total_revenue - total_expenses,
    }
    context.update(get_notification_context(request))
    return render(request, 'Home/accounts.html', context)


# ==================== Components ====================
@login_required
def components(request):
    context = {}
    context.update(get_notification_context(request))
    return render(request, 'Home/components.html', context)


# ==================== Welcome ====================
@login_required
def welcome(request):
    return render(request, 'authentication/welcome.html')

