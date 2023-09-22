from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("toggleTask/id/<int:id>/", views.toggleTask, name="toggleTask"),
  path("delete/id/<int:id>/", views.deleteTask, name="DeleteTask"),
  path("update/id/<int:id>/", views.updateTask, name="updateTask")
]