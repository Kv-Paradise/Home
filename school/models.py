from django.db import models
from django.contrib.auth.models import User
from student.models import Teacher

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# ==================== Department Model ====================
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ==================== Subject Model ====================
class Subject(models.Model):
    name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.subject_code})"


# ==================== Holiday Model ====================
class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)
    is_national_holiday = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


# ==================== Event Model ====================
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ==================== Library Model ====================
class LibraryBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    publication = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookIssue(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='book_issues')
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE, related_name='book_issues')
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.student.first_name}"


# ==================== Hostel Model ====================
class Hostel(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[('Boys', 'Boys'), ('Girls', 'Girls'), ('Mixed', 'Mixed')])
    total_rooms = models.IntegerField()
    available_rooms = models.IntegerField()
    warden_name = models.CharField(max_length=100)
    warden_contact = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class HostelRoom(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)
    room_type = models.CharField(max_length=50, choices=[('Single', 'Single'), ('Double', 'Double'), ('Triple', 'Triple')])
    fees_per_bed = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"


# ==================== Transport Model ====================
class TransportRoute(models.Model):
    route_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=15)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    stops = models.TextField(blank=True)  # JSON or comma-separated list of stops
    fees_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.route_name} - {self.vehicle_number}"


# ==================== Fees Collection Model ====================
class FeesCollection(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='fees')
    fees_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Online', 'Online'), ('Cheque', 'Cheque')])
    transaction_id = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Partial', 'Partial')], default='Pending')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.fees_type} - {self.amount}"


# ==================== Expense Model ====================
class Expense(models.Model):
    expense_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    vendor = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expense_type} - {self.amount}"


# ==================== Salary Model ====================
class Salary(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='salaries')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    bank_account = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.net_salary = self.base_salary + self.allowances - self.deductions
        super(Salary, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher.first_name} - {self.net_salary}"


# ==================== Time Table Model ====================
class TimeTable(models.Model):
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    day_of_week = models.CharField(max_length=20)
    period = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.class_name} - {self.day_of_week} - Period {self.period}"


# ==================== Exam Model ====================
class Exam(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_marks = models.IntegerField()
    passing_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject.name}"


# ==================== Sports Model ====================
class Sports(models.Model):
    name = models.CharField(max_length=100)
    coach_name = models.CharField(max_length=100)
    schedule = models.CharField(max_length=200, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
