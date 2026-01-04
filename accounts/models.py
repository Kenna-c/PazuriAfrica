from django.db import models
from django.utils.crypto import get_random_string

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    first_name = models.CharField(max_length=100, default="Pazuri")
    last_name = models.CharField(max_length=100, default="User")
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

class Staff(models.Model):
    staff_name = models.CharField(max_length=100, default="Pazuri Staff")
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    def generate_staff_id():
        return f"STF-{get_random_string(5).upper()}"
    staff_id = models.CharField(
        max_length=50,
        default=generate_staff_id,
        unique=True,
        blank=True,
        null=True
    )
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return f"Staff: {self.profile.user.username}"

class Instructor(models.Model):
    #lecturer = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='instructor_lecturer', default=None)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    hire_date = models.DateField()
    #staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='instructor_staff')
    department = models.CharField(max_length=100)
    office_location = models.CharField(max_length=100)

    def __str__(self):
        return f"Instructor: {self.profile.user.username}"

class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )

    admission_number = models.CharField(max_length=50, unique=True)
    admission_date = models.DateField()
    enrollment_date = models.DateField()
    is_active = models.BooleanField(default=True)

    lectures_attended = models.IntegerField(default=0)
    assignments_completed = models.IntegerField(default=0)

    def __str__(self):
        return f"Student: {self.profile.user.username}"


class AccountSettings(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"Settings for {self.user.username}"
class PaymentMethod(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    method_type = models.CharField(max_length=50)  # e.g., 'Credit Card', 'PayPal'
    details = models.TextField()  # JSON or plain text details
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.method_type} for {self.user.username}"

class Transaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)  # e.g., 'Pending', 'Completed', 'Failed'
    reference_code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Transaction {self.reference_code} for {self.user.username}"
