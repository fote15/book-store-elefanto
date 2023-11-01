"""
Database models
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from book.models import Book


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra):
        """Create save and return new user"""
        if not email:
            raise ValueError('User must have email')
        user = self.model(email=self.normalize_email(email), **extra)
        print(email)
        print(self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User base class"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    favourite_books = models.ManyToManyField(
        Book,
        related_name='users_added_to_favs',
        blank=True
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
