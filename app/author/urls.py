"""
URL mapping for recipe app
"""
from django.urls import (path)
from . import views


app_name = 'author'

urlpatterns = [
    path('all', views.get_all_authors, name='all-author'),
]
