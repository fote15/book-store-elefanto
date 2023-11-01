"""
Model for author module
"""
from django.db import models
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
