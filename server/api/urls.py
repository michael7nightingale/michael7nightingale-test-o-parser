from django.urls import path, include

from .docs import urlpatterns as docs_urlpatterns


urlpatterns = [
    path("docs/", include(docs_urlpatterns)),
    path("chats/", include("chats.urls")),
    path("", include("products.urls")),

]
