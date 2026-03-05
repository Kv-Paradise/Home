from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login, name='home'),
    path('dashboard/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('register/', views.register, name='signup'),
    path('forgot_password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('logout/', views.logout, name='logout'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    path('upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),
    path('change_password/', views.change_password, name='change_password'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    
    # Teachers
    path('teachers/', views.teachers, name='teachers'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('edit-teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('teacher-details/<int:teacher_id>/', views.teacher_details, name='teacher_details'),
    
    # Departments
    path('departments/', views.departments, name='departments'),
    path('add-department/', views.add_department, name='add_department'),
    path('edit-department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('delete-department/<int:department_id>/', views.delete_department, name='delete_department'),
    
    # Subjects
    path('subjects/', views.subjects, name='subjects'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    
    # Accounts & Fees
    path('accounts/', views.accounts, name='accounts'),
    path('fees-collections/', views.fees_collections, name='fees_collections'),
    path('add-fees/', views.add_fees, name='add_fees'),
    
    # Expenses
    path('expenses/', views.expenses, name='expenses'),
    path('add-expense/', views.add_expense, name='add_expense'),
    
    # Salary
    path('salary/', views.salary, name='salary'),
    path('add-salary/', views.add_salary, name='add_salary'),
    
    # Holiday
    path('holiday/', views.holiday, name='holiday'),
    path('add-holiday/', views.add_holiday, name='add_holiday'),
    path('delete-holiday/<int:holiday_id>/', views.delete_holiday, name='delete_holiday'),
    
    # Events
    path('events/', views.events, name='events'),
    path('add-event/', views.add_event, name='add_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    
    # Time Table
    path('time-table/', views.time_table, name='time_table'),
    path('add-timetable/', views.add_timetable, name='add_timetable'),
    
    # Library
    path('library/', views.library, name='library'),
    path('add-book/', views.add_book, name='add_book'),
    path('issue-book/', views.issue_book, name='issue_book'),
    
    # Sports
    path('sports/', views.sports, name='sports'),
    path('add-sport/', views.add_sport, name='add_sport'),
    
    # Hostel
    path('hostel/', views.hostel, name='hostel'),
    path('add-hostel/', views.add_hostel, name='add_hostel'),
    
    # Transport
    path('transport/', views.transport, name='transport'),
    path('add-route/', views.add_route, name='add_route'),
    
    # Exam
    path('exam-list/', views.exam_list, name='exam_list'),
    path('add-exam/', views.add_exam, name='add_exam'),
    
    # Components
    path('components/', views.components, name='components'),
]

