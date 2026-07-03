from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    class Gender(models.TextChoices):
        male= 'M','male'
        female= 'F','female'
        other= 'O','other'
    username = None
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=40,blank=False)
    city = models.CharField(max_length=30, blank=False)
    date_of_birth = models.DateField(blank=False)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=False)
    mobile_number = models.CharField(max_length=20, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
       
        "country",
        "city",
        "date_of_birth",
        "gender",
        "mobile_number",
    ]

    objects = UserManager()