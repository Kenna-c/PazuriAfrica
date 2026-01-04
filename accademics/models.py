from django.db import models

class Module(models.Model):
    program = models.ForeignKey(
        'programs.Program',
        on_delete=models.CASCADE,
        related_name='modules'
    )
    title = models.CharField(max_length=200)
    module_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    duration_weeks = models.IntegerField(default=1)
    lecturer = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'staff'},
        related_name='modules_teaching'
    )
    student = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        blank=True,
        null=True,
        related_name='modules_enrolled',
        default="Pazuri Student"
    )
    description = models.TextField()
    credits = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Result(models.Model):
    student = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    grade = models.CharField(max_length=2)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.user.username} - {self.module.code}"
class Attendance(models.Model):
    student = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('present', 'Present'), ('absent', 'Absent')))

    def __str__(self):
        return f"{self.student.user.username} - {self.module.code} on {self.date}"
class Assignment(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.title
class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE
    )
    submission_date = models.DateField()
    file = models.FileField(upload_to='assignments/')

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"
class Lecture(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=200)
    date = models.DateField()
    material = models.FileField(upload_to='lectures/', null=True, blank=True)

    def __str__(self):
        return f"{self.module.code} - {self.topic}"
class Fee(models.Model):
    student = models.OneToOneField(
        'accounts.Profile',
        on_delete=models.CASCADE
    )
    program = models.ForeignKey(
        'programs.Program',
        on_delete=models.CASCADE
    )
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def balance(self):
        return self.total_fees - self.paid_amount
    def __str__(self):
        return f"Fees for {self.student.user.username}"