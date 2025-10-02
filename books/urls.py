""""URL configuration for the books app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name='home'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('add-book/', views.add_book, name='add_book'),
]
