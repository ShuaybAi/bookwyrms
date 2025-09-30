"""Defines database models for users, books, reviews, and comments."""
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.
class CustomUser(AbstractUser):
    """Extends Django's AbstractUser to include a bio and profile image."""
    bio = models.TextField(blank=True)
    profile_image = CloudinaryField('profile_image', blank=True, null=True)

class Book(models.Model):
    """Represents a book uploaded by a user, including metadata and genre tags."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="books")
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published = models.DateField()
    cover = CloudinaryField('cover', blank=True, null=True)
    genres = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author} on {self.user.username}'s shelf"

class Review(models.Model):
    """Represents a user's review of a book including user, rating, content, and posted date."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviewers")
    rating = models.IntegerField()
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}"

class Comment(models.Model):
    """Represents a comment made by a user on a review, including content and approval status."""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="commenters")
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} on {self.review.book.title}"
