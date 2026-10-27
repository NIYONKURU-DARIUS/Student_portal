from django.db import models


class Student(models.Model):
    COURSE_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Software Engineering', 'Software Engineering'),
        ('Data Science', 'Data Science'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Information Technology', 'Information Technology'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES, default="Computer Science")
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=75.0, help_text="Grade percentage (0-100)")
    study_hours_per_week = models.FloatField(default=15.0, help_text="Weekly study hours")
    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'students'
        ordering = ['-id']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def status_badge(self):
        if self.grade >= 80:
            return "badge-success"
        elif self.grade >= 60:
            return "badge-primary"
        elif self.grade >= 50:
            return "badge-warning"
        return "badge-danger"

