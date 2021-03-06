from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("content/<str:name>/", views.content, name="content"),
    path("edit/<str:name>/", views.edit, name = "edit"),
    path("create/", views.create, name = "create"),
    path("create/<str:name>/", views.create_specific, name = "create_specific")
    
]
