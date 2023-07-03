from django.urls import path
from .views import index

urlpatterns = [
]


def new_playground(uuid: str):
	urlpatterns.append(path(f'{uuid}/', index))


new_playground('nnnnn')
print(type(urlpatterns[0].check()))


