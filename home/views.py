from django.shortcuts import render
from login import util
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def home(request):
    if util.is_twitter_authenticated(session_id=request.session.session_key):
        context = {}
        return render(request, "home/home.html", context)
    else:
        return HttpResponseRedirect("/")