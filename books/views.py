"""Views for the books app."""
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from .models import Book, Review, Comment
from .forms import BookForm, ReviewForm, CommentForm

# Create your views here.
class BookList(generic.ListView):
    """View to list all books."""
    queryset = Book.objects.all()
    template_name = 'books/book_list.html'

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
        # 'reviews': reviews,
        # 'comments': comments,
        # 'review_form': ReviewForm(),
        # 'comment_form': CommentForm(),
    })

# def add_book(request):
#     """View to add a new book."""
#     if request.method == 'POST':
#         form = BookForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = BookForm()
#     return render(request, 'add_book.html', {'form': form})

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
