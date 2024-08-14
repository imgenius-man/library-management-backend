from rest_framework.serializers import ModelSerializer
from .models import Author, Book, FavoriteBooks


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = FavoriteBooks
        fields = ['id', 'book']
