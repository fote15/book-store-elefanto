"""
Модели для модуля книг
"""
from django.db import models
from django.conf import settings
# Create your models here.
from author.models import Author
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save


class Book(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Админ создатель'
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='books'
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        verbose_name='Жанр книги',
        related_name='books'
    )
    rating = models.FloatField(null=True)
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    link = models.CharField(max_length=255, blank=True, verbose_name='Ссылка')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class BookReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name='Книга',
        related_name='reviews',
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    rating = models.IntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(0),
                    MaxValueValidator(5)],
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Genre(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Админ создатель'
    )
    title = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр книги'
        verbose_name_plural = 'Жанры книги'


def set_avarage_rating_for_book(sender, instance, created, **kwargs):
    if created:
        bk = Book.objects.get(pk=instance.book_id)
        reviews = bk.reviews.all()
        bk.rating = reviews.aggregate(models.Avg('rating')).get('rating__avg')
        bk.review_count = reviews.count()
        bk.save()


# Setting avarage review on book
post_save.connect(set_avarage_rating_for_book, sender=BookReview)
