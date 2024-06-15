from django.urls import path

from deprecated_authorization.views import index

urlpatterns = [
    path('', index)
]
