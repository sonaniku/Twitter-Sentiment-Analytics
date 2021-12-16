from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from login import util
# Create your views here.

def search(request):
    if util.is_twitter_authenticated(session_id=request.session.session_key):
        context = {}
        return render(request, "search_tweets/search_tweets.html", context)
    else:
        return HttpResponseRedirect("/")