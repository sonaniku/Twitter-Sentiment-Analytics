from django.urls import path 
from . import views
urlpatterns = [
    path('', views.apiOverview, name="apiOverview"),
    path('query-create/', views.Query_Add, name="query-add"),
    path('query-list/', views.Query_List, name='query-list'),
    path('query-filter/<str:query_id>/<str:date_created_at>', views.Dashboard_Filter, name="query-filter")
]
