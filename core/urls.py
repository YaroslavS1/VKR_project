# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include('registration.backends.default.urls')),  # Auth routes - login / register
    path("", include("apps.home.urls")),         # UI Kits Html files
    # path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
