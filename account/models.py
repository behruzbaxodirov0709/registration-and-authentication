from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
import string, random
from datetime import timedelta
from django.core.mail import send_mail
from django.utils import timezone




class CustomUser(AbstractUser):
    LANGUAGE_CHOICES = (
        ('uz', 'Uzbek'),
        ('ru', 'Russian'),
        ('eng', 'English')
    )
    AUTH_ROLE = (
        ('Customer', 'Customer'),
        ('Seller', 'Seller')
    )

    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=15, choices=AUTH_ROLE, default='Customer')
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=3, choices=LANGUAGE_CHOICES, default='uz')
    created_at = models.DateTimeField(auto_now_add=True)


    def token(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

    def __str__(self):
        return self.username


def code_generator():
    characters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    code = ''.join(characters[random.randint(0, len(characters)-1)] for _ in range(6))
    return code


class EmailOTP(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="otpcodes")
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = code_generator()

        if not self.expires_at:
            now = timezone.now()
            expiration_time = getattr(settings, 'EMAIL_EXPIRATION_TIME', 2)
            self.expires_at = now + timedelta(minutes=expiration_time)
        return super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired

    def __str__(self):
        return f"{self.user.email} - OTP"

