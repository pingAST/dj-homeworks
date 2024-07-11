from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    birth_date = models.DateField(null=True)


class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    students = models.ManyToManyField(Student, blank=True)

    def clean(self):
        if self.students.count() > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f"Максимальное число студентов на курсе: {settings.MAX_STUDENTS_PER_COURSE}")
