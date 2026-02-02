from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('edit/<slug:slug>/', views.edit_student, name='edit_student'),
    path('view/<slug:slug>/', views.view_student, name='view_student'),
    path('delete/<slug:slug>/', views.delete_student, name='delete_student'),
    path('mark-notifications-as-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('clear-all-notifications/', views.clear_all_notifications, name='clear_all_notifications'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('teacher-list/', views.teacher_list, name='teacher_list'),
    path('edit-teacher/<slug:slug>/', views.edit_teacher, name='edit_teacher'),
    path('view-teacher/<slug:slug>/', views.view_teacher, name='view_teacher'),
    path('delete-teacher/<slug:slug>/', views.delete_teacher, name='delete_teacher'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
]
