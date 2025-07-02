from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    User Registration System - Supports both Customer and Company registration
    Implements email uniqueness validation and dual user type system
    """
    email = models.EmailField(unique=True)  # Email uniqueness validation
    is_company = models.BooleanField(default=False)  # Company user type
    is_customer = models.BooleanField(default=False)  # Customer user type

class Customer(models.Model):
    """
    Customer Registration - Requires username, email, password, password confirmation, date of birth
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)  # Date of birth field

class Company(models.Model):
    """
    Company Registration - Requires username, email, password, password confirmation, field of work
    Field of work restricted to exact 12 predefined values
    """
    FIELD_CHOICES = [
        # Exact field restrictions as specified
        ("Air Conditioner", "Air Conditioner"),
        ("All in One", "All in One"),  # Special company type - can create any service type
        ("Carpentry", "Carpentry"),
        ("Electricity", "Electricity"),
        ("Gardening", "Gardening"),
        ("Home Machines", "Home Machines"),
        ("Housekeeping", "Housekeeping"),
        ("Interior Design", "Interior Design"),
        ("Locks", "Locks"),
        ("Painting", "Painting"),
        ("Plumbing", "Plumbing"),
        ("Water Heaters", "Water Heaters"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    field_of_work = models.CharField(max_length=70, choices=FIELD_CHOICES)  # Required field of work
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)  # Company rating system
