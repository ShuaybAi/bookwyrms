"""Admin configuration for the books app."""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import CustomUser, Book, Review, Comment

# Register your models here.
admin.site.register(CustomUser, SummernoteModelAdmin)
admin.site.register(Book, SummernoteModelAdmin)
admin.site.register(Review, SummernoteModelAdmin)
admin.site.register(Comment, SummernoteModelAdmin)
