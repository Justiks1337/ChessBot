from django.urls import path
from .views import main

urlpatterns = [
]


def new_playground(uuid: str):
	urlpatterns.append(path(f'{uuid}/', main))

