from django.urls import path, include


urlpatterns = [
    path("chats/", include("chats.urls")),
    path("", include("products.urls")),

]
