from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserListCreateAPIView.as_view()),
    path("<int:pk>/", views.UserDetailAPIView.as_view()),

    path("master/", views.MasterListCreateAPIView.as_view()),
    path("master/<int:pk>/", views.MasterDetailAPIView.as_view()),
    path("master/online-toggle/<int:pk>/", views.MasterOnlineToggleAPIView.as_view()),
]