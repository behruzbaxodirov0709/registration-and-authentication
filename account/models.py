from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    LANGUAGE_CHOICES = (
        ('uz', 'Uzbek'),
        ('ru', 'Russian'),
        ('eng', 'English')
    )
    AUTH_ROLE = (
        ('Customer', 'Customer'),
        ('Seller', 'Seller')
    )

    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=15, choices=AUTH_ROLE)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=3, choices=LANGUAGE_CHOICES, default='uz')

    def __str__(self):
        return self.username


    