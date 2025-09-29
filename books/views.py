from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    """A simple view that returns a welcome message."""
    return HttpResponse("Welcome to BookWyrms!")
