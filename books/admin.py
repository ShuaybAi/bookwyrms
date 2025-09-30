"""Admin configuration for the books app."""
from django.contrib import admin
from .models import CustomUser, Book, Review, Comment

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Comment)
