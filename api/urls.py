from django.urls import path
from .views import RegisterView, LoginView, AuthorList, AuthorDetail, BookList, BookDetail, FavoriteBooksView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('authors/', AuthorList.as_view()),
    path('authors/<int:pk>/', AuthorDetail.as_view()),
    path('books/', BookList.as_view()),
    path('books/<int:pk>/', BookDetail.as_view()),
    path('favorites/', FavoriteBooksView.as_view())
]
