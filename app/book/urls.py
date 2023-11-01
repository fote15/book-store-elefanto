"""
URL mapping for recipe app
"""
from django.urls import (path)
from . import views


app_name = 'books'

urlpatterns = [
    path('all', views.get_list_books, name='all-books'),
    path('detail', views.get_detail_book, name='all-books'),
    path('leave-review', views.leave_review, name='leave-review'),
    path('add-book-to-fav', views.add_book_to_fav, name='add-to-fav'),
]
