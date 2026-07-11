from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# handler404 = 'apps.user.views.custom_404'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("apps.user.urls")),
    path("api/category/", include("apps.category.urls")),
    path("api/application/", include("apps.application.urls")),
    path("api/review/", include("apps.review.urls")),
    path("api/notification/", include("apps.notification.urls")),
    path("api/subscription/", include("apps.subscription.urls")),

    path("api/token/", TokenObtainPairView.as_view()),
    path("api/refresh/", TokenRefreshView.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)