# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from ..authentication.models import CustomUser


# Create your models here.

class Campaign(models.Model):
    business = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=100)
    campaign = models.CharField(max_length=100)


class LikeCRM(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    visit = models.IntegerField(max_length=None)
    addto_cart = models.IntegerField(max_length=None)
    booking = models.IntegerField(max_length=None)
    payment = models.IntegerField(max_length=None)
    profit = models.DecimalField(max_digits=1000, decimal_places=2)


class LikeADV(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    impressions = models.IntegerField(max_length=None)
    clicks = models.IntegerField(max_length=None)
    cost = models.DecimalField(max_digits=1000, decimal_places=2)
