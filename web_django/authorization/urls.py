from django.urls import path
from authorization.views import index


urlpatterns = [
    path('', index),
]