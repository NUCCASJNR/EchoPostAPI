#!/usr/bin/env python3

"""Contains user class"""

from blog.models.base_model import BaseModel, models
from django.contrib.auth.models import AbstractUser


class MainUser(AbstractUser, BaseModel):
    """
    User model class
    """
    username = models.CharField(max_length=20, unique=True, blank=False)
    email = models.CharField(max_length=50, unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.set_password(self.password)
        super(MainUser, self).save(*args, **kwargs)
