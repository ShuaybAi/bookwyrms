"""Views for the books app."""
import json
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Count, Max
import cloudinary.uploader
from .models import Book, CustomUser
                 #, Review, Comment
from .forms import UserProfileForm, BookSearchForm
                #, BookForm, ReviewForm, CommentForm, BookSelectionForm
from .services import GoogleBooksService

# Create your views here.
def home(request):
    """View for the homepage."""
    return render(request, 'books/home.html')

class BookList(generic.ListView):
    """View to list all books."""
    queryset = Book.objects.all()
    template_name = 'books/book_list.html'
    paginate_by = 5  # Adjust the number of books per page as needed

def display_shelves(request):
    """View to display all book shelves grouped by user with pagination."""

    # Get all users who have books, ordered by username for consistency
    users_with_books = CustomUser.objects.filter(
        books__isnull=False
    ).annotate(
        book_count=Count('books'),
        last_book_added=Max('books__id')  # Assuming newer books have higher IDs
    ).distinct().order_by('-last_book_added')  # Most recent first

    # Set up pagination - show 3 users per page
    paginator = Paginator(users_with_books, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Group books by user for the current page
    books_by_user = []
    for user in page_obj:
        user_books = Book.objects.filter(user=user).order_by('-id')[:3]  # Show latest 3 books
        all_books_count = Book.objects.filter(user=user).count()
        books_by_user.append({
            'user': user,
            'books': user_books,
            'total_books': all_books_count,
            'has_more': all_books_count > 3  # Indicate if there are more than 3 books
        })

    return render(request, 'books/shelves.html', {
        'books_by_user': books_by_user,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator
    })

def user_shelf(request, username, user_id):
    """View to display all books for a specific user."""
    user = get_object_or_404(CustomUser, id=user_id)
    books = Book.objects.filter(user=user).order_by('-id')  # Show newest first
    return render(request, 'books/user_shelf.html', {
        'shelf_user': user,
        'books': books
    })

def book_detail(request, pk):
    """View to display a single book's details."""
    book = get_object_or_404(Book, pk=pk)

    # Get related books by same user
    user_books = Book.objects.filter(user=book.user).exclude(pk=pk)[:4]
    # reviews = book.reviews.all()
    # comments = book.comments.all()
    return render(request, 'books/book_detail.html', {
        'book': book,
        'user_books': user_books,
        # commented out for future use
        # 'reviews': reviews,
        # 'comments': comments,
        # 'review_form': ReviewForm(),
        # 'comment_form': CommentForm(),
    })

def delete_book(request, pk):
    """Delete a book from the user's shelf."""
    book = get_object_or_404(Book, pk=pk)

    if request.user != book.user:
        messages.add_message(
            request, messages.ERROR,
            'You do not have permission to delete this book.'
        )
        return redirect('book_detail', pk=pk)

    if request.method == "POST":
        title = book.title
        book.delete()
        messages.add_message(
            request, messages.SUCCESS,
            f'"{title}" has been removed from your shelf.'
        )
        return redirect('shelves')

    return redirect('book_detail', pk=pk)

@login_required
def search_books(request):
    """View to search for books using Google Books API."""
    if request.method == "POST":
        search_form = BookSearchForm(request.POST)
        if search_form.is_valid():
            title = search_form.cleaned_data['title']
            author = search_form.cleaned_data.get('author', '')

            # Search Google Books API
            api_results = GoogleBooksService.search_books(title, author)

            if api_results:
                # Store results in session for later use
                request.session['book_search_results'] = api_results

                # Convert each book dict to JSON string for the template
                for book in api_results:
                    book['json_data'] = json.dumps(book)

                return render(request, 'books/book_selection.html', {
                    'api_results': api_results,
                    'search_title': title,
                    'search_author': author
                })
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'No books found with that title and author. Please try different search terms.'
                )
    else:
        search_form = BookSearchForm()

    return render(request, 'books/search_books.html', {'form': search_form})


@login_required
@require_http_methods(["POST"])
def search_books_ajax(request):
    """AJAX endpoint for searching books via Google Books API."""
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()

        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)

        # Search Google Books API
        api_results = GoogleBooksService.search_books(title, author, max_results=10)

        return JsonResponse({
            'success': True,
            'results': api_results,
            'count': len(api_results)
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except (TypeError, ValueError) as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def add_book_from_api(request):
    """View to add a book from Google Books API selection."""
    if request.method == "POST":
        selected_book_data = request.POST.get('selected_book')

        if not selected_book_data:
            messages.add_message(
                request, messages.ERROR,
                'No book was selected. Please try again.'
            )
            return redirect('search_books')

        try:
            # Parse the selected book data
            print(f"DEBUG: Raw book data: {selected_book_data}")  # Debug line
            book_data = json.loads(selected_book_data)
            print(f"DEBUG: Parsed book data: {book_data}")  # Debug line

            # Check if book already exists for this user
            existing_book = Book.objects.filter(
                user=request.user,
                title__iexact=book_data.get('title', ''),
                author__iexact=book_data.get('author', '')
            ).first()
            
            if existing_book:
                messages.warning(request, f"'{book_data.get('title')}' is already in your shelf!")
                return redirect('search_books')

            # Create the book instance
            book = Book(
                user=request.user,
                title=book_data.get('title', ''),
                author=book_data.get('author', ''),
                description=book_data.get('description', ''),
                genres=book_data.get('genres', '')
                # Commented out for simplified version
                # google_books_id=book_data.get('google_books_id', ''),
                # isbn=book_data.get('isbn', ''),
                # publisher=book_data.get('publisher', ''),
                # page_count=book_data.get('page_count'),
                # rating=book_data.get('rating')
            )

            # Handle published date
            if book_data.get('published'):
                try:
                    # Parse ISO format date string from API
                    book.published = datetime.strptime(book_data['published'], '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    # Handle different date formats or invalid dates
                    try:
                        # Try parsing just year
                        year = int(book_data['published'][:4])
                        book.published = datetime(year, 1, 1).date()
                    except (ValueError, TypeError):
                        pass

            # Handle cover image download if URL provided
            cover_url = book_data.get('cover_url')
            if cover_url:
                try:
                    # Upload the cover image to Cloudinary
                    upload_result = cloudinary.uploader.upload(
                        cover_url,
                        folder="book_covers",
                        # Simplified naming
                        public_id=f"book_api_{request.user.id}_{str(book.title)[:20]}"
                        # Original with google_books_id
                        # public_id=f"book_{book.google_books_id or 'manual'}_{request.user.id}"
                    )
                    book.cover = upload_result['public_id']
                except cloudinary.exceptions.Error:
                    # If cover upload fails, continue without cover
                    messages.add_message(
                        request, messages.WARNING,
                        'Book added successfully, but cover image could not be downloaded.'
                    )

            book.save()

            messages.add_message(
                request, messages.SUCCESS,
                f'"{book.title}" has been added to your shelf!'
            )
            return redirect('book_detail', pk=book.pk)

        except json.JSONDecodeError:
            messages.add_message(
                request, messages.ERROR,
                'Invalid book data. Please try again.'
            )
        except (TypeError, ValueError, cloudinary.exceptions.Error) as e:
            messages.add_message(
                request, messages.ERROR,
                f'Error adding book: {str(e)}'
            )

    return redirect('search_books')


# @login_required
# def add_book(request):
#     """Legacy view for manual book addition (kept for backward compatibility)."""
#     if request.method == "POST":
#         book_form = BookForm(data=request.POST, files=request.FILES)
#         if book_form.is_valid():
#             book = book_form.save(commit=False)
#             book.user = request.user  # Assign the current user as the book owner
#             book.save()
#             messages.add_message(
#                 request, messages.SUCCESS,
#                 f'"{book.title}" has been added to your shelf!'
#             )
#             return redirect('book_detail', pk=book.pk)
#     else:
#         book_form = BookForm()

#     return render(
#         request,
#         'books/add_book.html', {'form': book_form})

# def add_review(request, book_id):
#     """View to add a review to a book."""
#     book = Book.objects.get(id=book_id)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.book = book
#             review.user = request.user
#             review.save()
#             return redirect('book_detail', pk=book.id)
#     else:
#         form = ReviewForm()
#     return render(request, 'add_review.html', {'form': form, 'book': book})

# def comment_edit(request, slug, comment_id):
#     """Displays an individual comment for editing."""
#     if request.method == "POST":

#         queryset = Book.objects.filter(status=1)
#         book = get_object_or_404(queryset, slug=slug)
#         comment = get_object_or_404(Comment, pk=comment_id)
#         comment_form = CommentForm(data=request.POST, instance=comment)

#         if comment_form.is_valid() and comment.author == request.user:
#             comment = comment_form.save(commit=False)
#             comment.book = book
#             comment.approved = False
#             comment.save()
#             messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
#         else:
#             messages.add_message(request, messages.ERROR, 'Error updating comment!')

#     return HttpResponseRedirect(reverse('post_detail', args=[slug]))

# def comment_delete(request, slug, comment_id):
#     """Deletes an individual comment if the user is the author."""
#     comment = get_object_or_404(Comment, pk=comment_id)

#     if comment.author == request.user:
#         comment.delete()
#         messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
#     else:
#         messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

#     return HttpResponseRedirect(reverse('book_detail', args=[slug]))

@login_required
def my_account(request):
    """View to display and edit user's account information"""
    return render(request, 'books/my_account.html')

@login_required
def edit_profile(request):
    """View to edit user's profile information."""
    if request.method == "POST":
        # Handle profile update
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Your profile has been updated successfully!'
            )
            return redirect('my_account')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'books/edit_profile.html', {'form': form})

@login_required
def remove_profile_image(request):
    """View to remove user's profile image."""
    user = request.user
    if request.method == "POST":
        if user.profile_image:
            try:
                # Extract the public_id from the Cloudinary URL
                public_id = user.profile_image.public_id
                # Delete from Cloudinary
                cloudinary.uploader.destroy(public_id)
                # Clear the field and save the user
                user.profile_image = None
                user.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    'Profile picture removed successfully!'
                )
            except cloudinary.exceptions.Error as e:
                messages.add_message(
                    request, messages.ERROR,
                    f'Error removing image: {str(e)}'
                )
        else:
            messages.add_message(
                request, messages.ERROR,
                'No profile picture to remove.'
            )
    return redirect('edit_profile')

@login_required
def delete_account(request):
    """View to permanently delete user account and all associated data."""
    if request.method == "POST":
        user = request.user
        username = user.username
        try:
            # Delete user's profile image from Cloudinary if it exists
            if user.profile_image:
                try:
                    public_id = user.profile_image.public_id
                    cloudinary.uploader.destroy(public_id)
                except cloudinary.exceptions.Error as e:
                    print(f"Error deleting profile image from Cloudinary: {e}")

            # Note: Django will cascade delete related objects (books, reviews, comments)
            # due to foreign key relationships with on_delete=CASCADE
            user.delete()

            # Add success message for the next request
            messages.success(
                request,
                f'Account: "{username}" has been permanently deleted. We\'re sorry to see you go!'
            )

            # Redirect to home page since user no longer exists
            return redirect('home')

        except (user.DoesNotExist, cloudinary.exceptions.Error) as e:
            print(f"Error deleting account for {username}: {e}")
            messages.error(
                request,
                'An error occurred while deleting your account. Please try again.'
            )
            return redirect('my_account')

    # If GET request, redirect to account page (shouldn't happen with the modal setup)
    return redirect('my_account')
