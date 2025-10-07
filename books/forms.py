"""Forms for the books app."""
from django import forms
from .models import Book, Review, Comment, CustomUser


class BookSearchForm(forms.Form):
    """Initial form for searching books via Google Books API."""
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter book title...',
            'required': True
        })
    )
    author = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter author name (optional)...'
        })
    )


class BookSelectionForm(forms.Form):
    """Form for selecting a book from Google Books API results."""
    selected_book = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        self.api_results = kwargs.pop('api_results', [])
        super().__init__(*args, **kwargs)


class BookForm(forms.ModelForm):
    """Form for adding or editing a book with all fields."""
    class Meta:
        model = Book
        fields = ['title', 'author', 'published', 'genres', 'description', 'cover']
                 # 'google_books_id', 'isbn', 'publisher', 'page_count', 'rating']  # Commented out for simplified version
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'published': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genres': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cover': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
            # 'google_books_id': forms.HiddenInput(),
            # 'isbn': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            # 'publisher': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            # 'page_count': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            # 'rating': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True, 'step': '0.1'})
        }

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

class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information."""
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_image']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address...'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name...'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name...'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself and your reading interests...'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
