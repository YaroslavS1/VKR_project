# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.urls import path, include  # add this
from apps.home.dash_apps.finished_apps import simpleexample

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('funnel/', views.funnel, name='funnel'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
