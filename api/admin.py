from django.contrib import admin
from .models import Book, Author, FavoriteBooks

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(FavoriteBooks)
