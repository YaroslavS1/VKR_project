# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.

from apps.authentication.models import CustomUser


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = CustomUser.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        print(field_label)
        self.assertEquals(field_label, 'first name')

    def test_date_of_death_label(self):
        author = CustomUser.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        print(author)
        self.assertEquals(author, 'died')
