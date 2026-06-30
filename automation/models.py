from django.db import models


class Employee(models.Model):
    
    DEPARTMENT_CHOICES = [
            ("SALES", "Sales"),
            ("OPS", "Operations"),
            ("IT", "IT"),
            ("DEV", "Software Developer"),
            ("DEV_INTERN", "Developer Intern"),
            ("HR", "Human Resources"),
        ]
    
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    
    department = models.CharField(max_length=20, choices= DEPARTMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DailySubmission(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    submission_date = models.DateField(auto_now_add=True)

    task_1 = models.TextField()
    task_2 = models.TextField()
    task_3 = models.TextField()

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "submission_date"],
                name="unique_daily_submission"
            )
        ]
        ordering = ["-submitted_at"]


    def __str__(self):
        return f"{self.employee.name} - {self.submission_date}"


class ProgressUpdate(models.Model):
    submission = models.OneToOneField(
        DailySubmission,
        on_delete=models.CASCADE,
        related_name="progress"
    )

    completed_tasks = models.TextField(blank=True)
    pending_tasks = models.TextField(blank=True)
    challenges = models.TextField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Progress Update - {self.submission.employee.name}"