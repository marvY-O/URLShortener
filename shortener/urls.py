from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('shorten/', views.shorten),
    path('<str:shortID>/', views.RetrieveURL.as_view()),
]