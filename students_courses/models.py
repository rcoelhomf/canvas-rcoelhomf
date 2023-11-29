from django.db import models
import uuid
from courses.models import Course
from accounts.models import Account


class StudentCourseStatus(models.TextChoices):
    PENDING = 'pending'
    ACCEPTED = 'accepted'


class StudentCourse(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    status = models.CharField(max_length=20, choices=StudentCourseStatus.choices, default=StudentCourseStatus.PENDING)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students_courses')
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='students_courses')
