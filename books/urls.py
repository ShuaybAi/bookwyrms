""""URL configuration for the books app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shelves/', views.BookList.as_view(), name='book_list'),
    path('shelves/book/<int:pk>/', views.book_detail, name='book_detail'),
    path('add-book/', views.add_book, name='add_book'),
    path('my-account/', views.my_account, name='my_account'),
    path('my-account/edit-profile/', views.edit_profile, name='edit_profile'),
    path('remove-profile-image/', views.remove_profile_image, name='remove_profile_image'),
    # path('my-account/delete-account/', views.delete_account, name='delete_account'),
]
