from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("room/<str:pk>/", views.room, name="room"),

    path("create_room", views.create_room, name="create_room"),
    path("update-room/<str:pk>/", views.updateroom, name="update-room"),
    path("delete-room/<str:pk>/", views.deleteroom, name="delete-room"),

]