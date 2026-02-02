from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.contrib import messages
# Create your views here.

def create_notification(user, message):
    from .models import Notification
    if user.is_authenticated:
        Notification.objects.create(user=user, message=message)


def mark_notifications_as_read(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'})
        
        notification_id = request.POST.get('notification_id')
        if notification_id:
            try:
                notification = Notification.objects.get(id=notification_id, user=request.user)
                notification.is_read = True
                notification.save()
                return JsonResponse({'status': 'success'})
            except Notification.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Notification not found'})
        else:
            # Mark all notifications as read
            request.user.notification_set.filter(is_read=False).update(is_read=True)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def clear_all_notifications(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'})
        
        request.user.notification_set.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        # Retrieve parent data from the form
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        # save parent information
        parent = Parent.objects.create(
            father_name= father_name,
            father_occupation= father_occupation,
            father_mobile= father_mobile,
            father_email= father_email,
            mother_name= mother_name,
            mother_occupation= mother_occupation,
            mother_mobile= mother_mobile,
            mother_email= mother_email,
            present_address= present_address,
            permanent_address= permanent_address
        )

        # Save student information
        student = Student.objects.create(
            first_name= first_name,
            last_name= last_name,
            student_id= student_id,
            gender= gender,
            date_of_birth= date_of_birth,
            student_class= student_class,
            religion= religion,
            joining_date= joining_date,
            mobile_number = mobile_number,
            admission_number = admission_number,
            section = section,
            student_image = student_image,
            parent = parent
        )
        create_notification(request.user, f"Added Student: {student.first_name} {student.last_name}")
        messages.success(request, "Student added Successfully")
        return redirect("student:student_list")

  

    unread_notification_count = 0
    unread_notification = []
    if request.user.is_authenticated:
        unread_notification = request.user.notification_set.filter(is_read=False)
        unread_notification_count = unread_notification.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notification
    }
    return render(request,"students/add-student.html", context)



def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    unread_notification_count = 0
    unread_notification = []
    if request.user.is_authenticated:
        unread_notification = request.user.notification_set.filter(is_read=False)
        unread_notification_count = unread_notification.count()
    context = {
        'student_list': student_list,
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notification
    }
    return render(request, "students/students.html", context)


def edit_student(request,slug):
    student = get_object_or_404(Student, slug=slug)
    parent = student.parent if hasattr(student, 'parent') else None
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')  if request.FILES.get('student_image') else student.student_image

        # Retrieve parent data from the form
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')
        parent.save()

#  update student information

        student.first_name= first_name
        student.last_name= last_name
        student.student_id= student_id
        student.gender= gender
        student.date_of_birth= date_of_birth
        student.student_class= student_class
        student.religion= religion
        student.joining_date= joining_date
        student.mobile_number = mobile_number
        student.admission_number = admission_number
        student.section = section
        student.student_image = student_image
        student.save()
        context = {
            'student': student,
            'parent': parent,
            }
        create_notification(request.user, f"Updated Student: {student.first_name} {student.last_name}")

        return redirect("student:student_list")
    unread_notification_count = 0
    unread_notification = []
    if request.user.is_authenticated:
        unread_notification = request.user.notification_set.filter(is_read=False)
        unread_notification_count = unread_notification.count()
    context = {
        'student': student,
        'parent': parent,
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notification
    }
    return render(request, "students/edit-student.html", context)


def view_student(request, slug):
    student = get_object_or_404(Student, student_id = slug)
    context = {
        'student': student
    }
    return render(request, "students/student-details.html", context)


def delete_student(request,slug):
    if request.method == "POST":
        student = get_object_or_404(Student, slug=slug)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()
        create_notification(request.user, f"Deleted student: {student_name}")
        return redirect ('student_list')
    return HttpResponseForbidden()


def add_teacher(request):
    if request.method == "POST":
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
        teacher_image = request.FILES.get('teacher_image')

        # Save teacher information
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
            teacher_image=teacher_image,
        )
        create_notification(request.user, f"Added Teacher: {teacher.first_name} {teacher.last_name}")
        messages.success(request, "Teacher added Successfully")
        return redirect("student:teacher_list")

    unread_notification_count = 0
    unread_notification = []
    if request.user.is_authenticated:
        unread_notification = request.user.notification_set.filter(is_read=False)
        unread_notification_count = unread_notification.count()
    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notification
    }
    return render(request,"teachers/add-teacher.html", context)


def teacher_list(request):
    teacher_list = Teacher.objects.all()
    unread_notification_count = 0
    unread_notification = []
    if request.user.is_authenticated:
        unread_notification = request.user.notification_set.filter(is_read=False)
        unread_notification_count = unread_notification.count()
    context = {
        'teacher_list': teacher_list,
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notification
    }
    return render(request, "teachers/teacher-list.html", context)


def edit_teacher(request,slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    if request.method == "POST":
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
        teacher_image = request.FILES.get('teacher_image') if request.FILES.get('teacher_image') else teacher.teacher_image

        teacher.first_name = first_name
        teacher.last_name = last_name
        teacher.teacher_id = teacher_id
        teacher.gender = gender
        teacher.date_of_birth = date_of_birth
        teacher.qualification = qualification
        teacher.specialization = specialization
        teacher.mobile_number = mobile_number
        teacher.email = email
        teacher.joining_date = joining_date
        teacher.department = department
        teacher.teacher_image = teacher_image
        teacher.save()

        create_notification(request.user, f"Updated Teacher: {teacher.first_name} {teacher.last_name}")
        messages.success(request, "Teacher updated Successfully")
        return redirect("student:teacher_list")

    unread_notification_count = 0
    unread_notification = []
    if request.user.is_authenticated:
        unread_notification = request.user.notification_set.filter(is_read=False)
        unread_notification_count = unread_notification.count()
    context = {
        'teacher': teacher,
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notification
    }
    return render(request, "teachers/edit-teacher.html", context)


def view_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)
    context = {
        'teacher': teacher
    }
    return render(request, "teachers/teacher-details.html", context)


def delete_teacher(request,slug):
    if request.method == "POST":
        teacher = get_object_or_404(Teacher, slug=slug)
        teacher_name = f"{teacher.first_name} {teacher.last_name}"
        teacher.delete()
        create_notification(request.user, f"Deleted teacher: {teacher_name}")
        return redirect ('student:teacher_list')
    return HttpResponseForbidden()


def student_dashboard(request):
    unread_notification_count = 0
    unread_notification = []
    if request.user.is_authenticated:
        unread_notification = request.user.notification_set.filter(is_read=False)
        unread_notification_count = unread_notification.count()

    # Fetch database data for dashboard
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_notifications = Notification.objects.filter(user=request.user).count()
    total_revenue = Revenue.objects.count()  # Assuming revenue as a proxy for projects or something

    context = {
        'unread_notification_count': unread_notification_count,
        'unread_notification': unread_notification,
        'user_name': request.user.first_name or request.user.username,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_notifications': total_notifications,
        'total_revenue': total_revenue,
    }
    return render(request, "students/student-dashboard.html", context)
