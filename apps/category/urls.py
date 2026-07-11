from django.urls import path
from . import views

urlpatterns = [
    path("", views.CategoryListCreateAPIView.as_view()),
    path("<int:pk>/", views.CategoryDetailAPIView.as_view()),
]