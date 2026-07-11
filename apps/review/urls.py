from django.urls import path
from . import views

urlpatterns = [
    path("", views.ReviewListCreateAPIView.as_view()),
    path("<int:pk>/", views.ReviewDetailAPIView.as_view()),
]