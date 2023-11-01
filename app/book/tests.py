import datetime
from django.test import TestCase # noqa
from django.contrib.auth import get_user_model
# Create your tests here.
from .models import Genre, Book
from author.models import Author
from rest_framework.test import APIClient


class BookFavAddingAPITest(TestCase):
    """Test unauthed user error"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_adding_book_to_fav(self):
        user_data = {
            'email': 'example2@example.com',
            'password': 'qwerty12',
        }
        self.user = get_user_model().objects.create(**user_data)
        self.client.force_authenticate(self.user)
        genre = Genre.objects.create(user=self.user, title='test')
        author = Author.objects.create(name='Test Author')
        defaults = {
            'user': self.user,
            'author': author,
            'genre': genre,
            'rating': 5,
            'description': 'test',
            'price': 1000,
            'is_active': True,
            'link': "test",
            'created_at': datetime.datetime.today(),
            'updated_at': datetime.datetime.today(),

        }
        book = Book.objects.create(**defaults)
        book_in_fav = self.user.favourite_books.filter(id=book.id).exists()
        self.assertEqual(book_in_fav, False)
        self.user.favourite_books.add(book)
        book_in_fav = self.user.favourite_books.filter(id=book.id).exists()
        self.assertEqual(book_in_fav, True)
