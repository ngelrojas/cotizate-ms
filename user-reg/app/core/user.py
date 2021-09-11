from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """create and save a new users"""
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email.lower()), **extra_fields)
        user.is_activate = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create and save new superuser"""
        user = self.create_user(email.lower(), password)
        user.is_activate = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username"""

    TYPE_USER = ((1, "contributor"), (2, "creator"))
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    type_user = models.PositiveSmallIntegerField(choices=TYPE_USER, default=1)
    deleted = models.BooleanField(default=False)
    is_activate = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
