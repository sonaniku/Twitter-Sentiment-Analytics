from django.urls import path
from . import views
urlpatterns = [
    path('', views.login, name='login'),
    #path('<str:pk>', views.test, name="test"),
    #path('', views.TwitterCallbackEndpoint.as_view()),
    
    path(
        "auth/twitter/redirect/",
        views.TwitterAuthRedirectEndpoint.as_view(),
        name="twitter-login-redirect",
   ),
   path(
    "callback/twitter/",
     views.TwitterCallbackEndpoint.as_view(),
     name="twitter-login-callback",
   ),
   path('is-authenticated', views.IsAuthenticated.as_view())
]