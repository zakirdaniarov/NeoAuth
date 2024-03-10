from django.urls import path
from .views import RegisterAPIView, EmailVerificationAPIView, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('email-activate/', EmailVerificationAPIView.as_view(), name='email-verification'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
