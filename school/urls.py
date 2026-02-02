from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='home'),
    path('dashboard/', views.index, name='index'),

    path('login/', views.login, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('register/', views.register, name='signup'),
    path('forgot_password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),
    path('change_password/', views.change_password, name='change_password'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('departments/', views.departments, name='departments'),
    path('subjects/', views.subjects, name='subjects'),
    path('accounts/', views.accounts, name='accounts'),
    path('holiday/', views.holiday, name='holiday'),
    path('exam-list/', views.exam_list, name='exam_list'),
    path('events/', views.events, name='events'),
    path('time-table/', views.time_table, name='time_table'),
    path('library/', views.library, name='library'),
    path('sports/', views.sports, name='sports'),
    path('hostel/', views.hostel, name='hostel'),
    path('transport/', views.transport, name='transport'),
    path('components/', views.components, name='components'),
]
