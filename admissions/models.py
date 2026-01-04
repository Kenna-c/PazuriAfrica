from django.db import models
from django.utils.crypto import get_random_string



class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    program = models.ForeignKey('programs.Program', on_delete=models.CASCADE, related_name='applications')

    # admission number generator
    def generate_admission_no():
        return f"PAC-{get_random_string(6).upper()}"

    admission_number = models.CharField(
        max_length=50,
        default=generate_admission_no,
        unique=True,
        blank=True,
        null=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    id_copy = models.FileField(upload_to='applications/id_copies/')
    certificate = models.FileField(upload_to='applications/certificates/')
    # application code generator
    def generate_application_code():
        return get_random_string(12)

    application_code = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=generate_application_code
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program}"
