from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def search(request):
    
    
    context = {}
    return render(request, "search_tweets/search_tweets.html", context)