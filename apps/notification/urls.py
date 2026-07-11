from django.urls import path
from . import views

urlpatterns = [
    path("", views.NotificationListCreateAPIView.as_view()),
    path("<int:pk>/", views.NotificationDetailAPIView.as_view()),
]