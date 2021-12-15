from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse
#from requests import status_codes
from requests_oauthlib import OAuth1
from requests_oauthlib import requests
from urllib.parse import urlencode
#from rest_framework import settings
from rest_framework.views import APIView
from django.http.response import HttpResponseRedirect
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import is_twitter_authenticated, update_or_create_user_token, get_user_tokens
from main.settings import CONSUMER_KEY, CONSUMER_SECRET, REDIRECT_URI
# Create your views here.
def login(request):
    return render(request, "login/login.html", {})
""""""
class TwitterAuthRedirectEndpoint(APIView):
    def get(self, request, *args, **kwargs):
        if not is_twitter_authenticated(session_id=request.session.session_key):
            try:
                oauth = OAuth1(
                    client_key= CONSUMER_KEY,
                    client_secret= CONSUMER_SECRET
                )
                #Step one: obtaining request token
                request_token_url = "https://api.twitter.com/oauth/request_token"
                data = urlencode({
                    "oauth_callback": REDIRECT_URI 
                })
                response = requests.post(request_token_url, auth=oauth, data=data)
                response.raise_for_status()
                response_split = response.text.split("&")
                oauth_token = response_split[0].split("=")[1]
                oauth_token_secret = response_split[1].split("=")[1]
                
                #Step two: redirecting user to Twitter
                twitter_redirect_url = (
                    f"https://api.twitter.com/oauth/authenticate?oauth_token={oauth_token}"
                )
                return HttpResponseRedirect(twitter_redirect_url)
            except ConnectionError:
                html = "<html><body>You have no internet connection</body></html>"
                return HttpResponse(html, status=403)
            except Exception as ex:
                html="<html><body>Something went wrong. Try Again</body></html>"
                print(ex)
                return HttpResponse(html, status=403)
        else: return HttpResponseRedirect('/home')
class TwitterCallbackEndpoint(APIView):
    def get(self, request, *args, **kwargs):
        try:
            oauth_token = request.query_params.get("oauth_token")
            oauth_verifier = request.query_params.get("oauth_verifier")
            oauth = OAuth1(
                client_key= CONSUMER_KEY,
                client_secret= CONSUMER_SECRET,
                resource_owner_key=oauth_token,
                verifier=oauth_verifier,
            )
            res = requests.post(
                f"https://api.twitter.com/oauth/access_token", auth=oauth
            )
            res_split = res.text.split("&")
            oauth_token=res_split[0].split("=")[1]
            oauth_secret=res_split[1].split("=")[1]
            user_id = res_split[2].split("=")[1] if len(res_split) > 2 else None
            user_name = res_split[3].split("=")[1] if len(res_split) > 3 else None 
            if not request.session.exists(request.session.session_key):
                request.session.create()
            update_or_create_user_token(request.session.session_key, oauth_token,
            oauth_secret, user_id, user_name)
            ##
            redirect_url="http://127.0.0.1:8000/home/"
            return HttpResponseRedirect(redirect_url)
        except ConnectionError:
            return HttpResponse(
                "<html><body>You have no internet connection</body></html>", status=403
            )
        except Exception as ex:
            print(ex)
            return HttpResponse(
                "<html><body>Something went wrong.Try again.</body></html>", status=403
            )

class IsAuthenticated(APIView):
    def get(self, request, *args, **kwargs):
        is_authenticated = is_twitter_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


