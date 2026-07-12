from django.urls import path
from . import views

urlpatterns = [
    path("", views.ApplicationListCreateAPIView.as_view()),
    path("<int:pk>/", views.ApplicationDetailAPIView.as_view()),
    path("<int:pk>/accept/", views.ApplicationAcceptAPIView.as_view()),

]