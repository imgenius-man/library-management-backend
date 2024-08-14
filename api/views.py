from .models import Author, Book, FavoriteBooks
from .serializers import AuthorSerializer, BookSerializer, FavoriteSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.db.models import Q
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class AuthorList(APIView):

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetail(APIView):

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def put(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookList(APIView):

    def get(self, request):
        query = request.GET.get('search')
        if query:
            books = Book.objects.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)
            )
        else:
            books = Book.objects.all()

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username, password=password, email=email)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class FavoriteBooksView(APIView):
    def get(self, request):
        user = request.user
        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        favorites = FavoriteBooks.objects.filter(user=user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        favorite = FavoriteBooks.objects.filter(
            user=user, book_id=book_id).first()

        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Book not found in your favorites."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        if FavoriteBooks.objects.filter(user=user).count() >= 20:
            return Response({"error": "You can't have more than 20 favorite books."},
                            status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.get(id=book_id)
        favorite, created = FavoriteBooks.objects.get_or_create(
            user=user, book=book)
        if not created:
            return Response({"error": "This book is already in your favorites."},
                            status=status.HTTP_400_BAD_REQUEST)
        recommended_books = self.get_recommendations(user, book.title)
        serializer = BookSerializer(recommended_books, many=True)

        return Response({
            "favorite": FavoriteSerializer(favorite).data,
            "recommended": serializer.data
        }, status=status.HTTP_201_CREATED)

    def get_recommendations(self, user, book_title):
        favorite_books = FavoriteBooks.objects.filter(
            user=user).values_list('book__title', flat=True)
        all_books = Book.objects.exclude(title=book_title)
        combined_titles = list(favorite_books) + \
            [book.title for book in all_books]
        combined_titles.append(book_title)
        vectorizer = TfidfVectorizer().fit_transform(combined_titles)
        vectors = vectorizer.toarray()
        cosine_similarities = cosine_similarity(
            vectors[-1].reshape(1, -1), vectors[:-1]).flatten()
        similar_indices = cosine_similarities.argsort()[-5:][::-1]
        similar_indices = [int(i) for i in similar_indices]
        recommended_books = [Book.objects.get(
            title=combined_titles[i]) for i in similar_indices]

        return recommended_books
