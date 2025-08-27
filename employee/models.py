from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name