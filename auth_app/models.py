from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, validate_email
from django.db import models

# Validator for phone number
phone_regex = RegexValidator(
    regex=r"^\d{10}$", message="Phone number must be 10 digits only."
)

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(self, email=None, username=None, phone_number=None, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
        """
        if not email and not username:
            raise ValueError("The Email or Username field must be set")
        
        email = self.normalize_email(email) if email else None
        username = self.model.normalize_username(username) if username else None
        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, username=None, phone_number=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email=email, username=username, phone_number=phone_number, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model.
    """

    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True, null=True, blank=True, validators=[validate_email])
    phone_number = models.CharField(max_length=10, null=True, blank=True, validators=[phone_regex])

    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    user_registered_at = models.DateTimeField(auto_now_add=True)
    
    NOTIFICATION_CHOICES = [
        (1, '1 day before'),
        (2, '2 days before'),
        (3, '3 days before'),
        (4, '4 days before'),
        (4, '4 days before'),
        (5, '5 days before'),
        (6, '6 days before'),
        (7, '7 days before'),       
    ]
    notification_preference = models.IntegerField(choices=NOTIFICATION_CHOICES, default=1)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email or f"User ID: {self.id}"
