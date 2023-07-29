from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

from main.latter.models import NULLABLE, SmsLetter


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    product = models.ForeignKey(SmsLetter, on_delete=models.CASCADE, **NULLABLE)

    avatar = models.ImageField(upload_to="users/", verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name="телефон")
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class UserVerification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

from django.db import models

# Create your models here.
