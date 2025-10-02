"""Forms for the books app."""
from django import forms
from .models import Book, Review, Comment


class BookForm(forms.ModelForm):
    """Form for adding or editing a book."""
    class Meta:
        model = Book
        fields = ['title', 'author']  # Other fields will be added through taking details from api
        # fields = ['title', 'author', 'published', 'genres', 'cover', 'description']
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Enter book title...'
        #     }),
        #     'author': forms.TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Enter author name...'
        #     }),
        #     'published': forms.DateInput(attrs={
        #         'class': 'form-control',
        #         'type': 'date'
        #     }),
        #     'genres': forms.TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Fiction, Romance, Mystery...'
        #     }),
        #     'cover': forms.FileInput(attrs={
        #         'class': 'form-control',
        #         'accept': 'image/*'
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': 'form-control',
        #         'rows': 4,
        #         'placeholder': 'Enter a brief description of the book...'
        #     })
        # }

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
