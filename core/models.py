from django.db import models
from django.contrib.auth.models import User

# Bus Model
class Bus(models.Model):
    bus_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, default='active')
    def __str__(self):
        return self.title

# Admin Model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.user.username

# Supervisor Model
class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.username

# Driver Model
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    assigned_bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.username


# Student Model

class Student(models.Model):
    fname = models.CharField(max_length=30, blank=True, default='')
    lname = models.CharField(max_length=30, blank=True, default='')
    father = models.CharField(max_length=30, blank=True, default='')
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
    student_class = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=20, blank=True, default='')
    dob = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='students/', null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=200, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    registration_code = models.CharField(max_length=50, blank=True, default='')
    reg_code_status = models.CharField(max_length=20, choices=[('active', 'Active'), ('used', 'Used')], default='active')
    request_date = models.DateField(null=True, blank=True)
    request_time = models.TimeField(null=True, blank=True)
    request = models.CharField(max_length=255, null=True, blank=True)
    qrcode = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"


# Guardian Model
class Guardian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    students = models.ManyToManyField(Student, related_name='guardians')
    def __str__(self):
        return self.user.username

# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)  # Present/Absent
    def __str__(self):
        return f"{self.student} - {self.date}"

# Announcement Model
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

# Bus Assignment Model
class BusAssignment(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assigned_date = models.DateField()
    def __str__(self):
        return f"{self.student} -> {self.bus}"

# Bus Route Model
class BusRoute(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route_name = models.CharField(max_length=100)
    def __str__(self):
        return self.route_name

# Bus Route Point Model

class BusRoutePoint(models.Model):
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=100)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.location_name

# Trip Model
class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.bus} - {self.date}"

# Trip Students Model
class TripStudent(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.student} on {self.trip}"

# Feedback Model
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Feedback by {self.user.username}"

# Maintenance Log Model
class MaintenanceLog(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    def __str__(self):
        return f"{self.bus} - {self.maintenance_type}"

# Notification Model
class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.title

# Reminder Model
class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    remind_at = models.DateTimeField()
    def __str__(self):
        return f"Reminder for {self.user.username}"

# GPS Tracking Model


class GPSTracking(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, default=0.0)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.bus} @ {self.timestamp}"

# Class Model
class Class(models.Model):
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=20)
    def __str__(self):
        return self.name
