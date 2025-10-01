"""Forms for the books app."""
from django import forms
from .models import Book, Review, Comment


class BookForm(forms.ModelForm):
    """Form for adding or editing a book."""
    class Meta:
        model = Book
        fields = ['title', 'author']  # Other fields will be added through taking details from api

class ReviewForm(forms.ModelForm):
    """Form for adding or editing a book review."""
    class Meta:
        model = Review
        fields = ['rating', 'content']  # 'book' and 'user' will be set in the view

class CommentForm(forms.ModelForm):
    """Form for adding or editing a comment on a review."""
    class Meta:
        model = Comment
        fields = ['content']  # 'review' and 'user' will be set in the view
