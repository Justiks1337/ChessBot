from django.urls import path

from views import add_to_blacklist, in_blacklist, remove_from_blacklist


urlpatterns = [
    path("in_blacklist", in_blacklist),
    path("add_to_blacklist", add_to_blacklist),
    path("remove_from_blacklist", remove_from_blacklist)

]