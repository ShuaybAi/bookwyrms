""""URL configuration for the books app."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name='home'),
]
