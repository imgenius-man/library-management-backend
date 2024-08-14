from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class FavoriteBooks(models.Model):
    user = models.ForeignKey(User, related_name='users',
                             on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='books',
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')
