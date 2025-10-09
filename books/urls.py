""""URL configuration for the books app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.BookList.as_view(), name='book_list'),
    path('shelves/', views.display_shelves, name='shelves'),
    path('shelves/user/<str:username>-<int:user_id>/', views.user_shelf, name='user_shelf'),
    path('shelves/book/<int:pk>/', views.book_detail, name='book_detail'),
    path('shelves/book/<int:pk>/delete/', views.delete_book, name='delete_book'),
    # Book addition URLs - API search is now primary method
    path('add-book/', views.search_books, name='add_book'),  # Redirect add-book to API search
    path('search-books/', views.search_books, name='search_books'),
    path('search-books-ajax/', views.search_books_ajax, name='search_books_ajax'),
    path('add-book-from-api/', views.add_book_from_api, name='add_book_from_api'),
    # path('add-book-manual/', views.add_book, name='add_book_manual'),  # Commented out manual add
    path('my-account/', views.my_account, name='my_account'),
    path('my-account/edit-profile/', views.edit_profile, name='edit_profile'),
    path('my-account/edit-profile/remove-profile-image/',
         views.remove_profile_image, name='remove_profile_image'),
    path('my-account/delete-account/', views.delete_account, name='delete_account'),
]
