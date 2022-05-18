# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # business = models.URLField(max_length=100, default=None, blank=True, null=True)
    # add additional fields in here

    def __str__(self):
        return self.username

    app_label = 'apps.home'