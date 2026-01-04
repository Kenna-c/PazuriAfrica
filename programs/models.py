from django.db import models

class Program(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    STUDY_MODE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('online', 'Online'),
    ]

    STUDY_LEVEL_CHOICES = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('degree', 'Degree'),
        ('postgraduate', 'Postgraduate'),
    ]

    program_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    study_mode = models.CharField(max_length=20, choices=STUDY_MODE_CHOICES)
    study_level = models.CharField(max_length=20, choices=STUDY_LEVEL_CHOICES)
    duration_months = models.IntegerField(default=6)

    


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



# class ProgramApplication(models.Model):
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='applications')
#     applicant_name = models.CharField(max_length=200)
#     applicant_email = models.EmailField()
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, default='Pending')

#     def __str__(self):
#         return f"{self.applicant_name} - {self.program.name}"