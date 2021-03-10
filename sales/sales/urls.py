from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
)

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
