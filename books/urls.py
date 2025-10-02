""""URL configuration for the books app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shelves/', views.BookList.as_view(), name='book_list'),
    path('shelves/book/<int:pk>/', views.book_detail, name='book_detail'),
    path('add-book/', views.add_book, name='add_book'),
    path('my-account/', views.my_account, name='my_account'),
]
