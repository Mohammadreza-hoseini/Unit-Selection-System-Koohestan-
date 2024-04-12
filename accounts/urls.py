from django.urls import path, include
from .views import RequestOTPView, ChangePassword
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password_request/', RequestOTPView.as_view(), name="change_password_request"),
    path('change_password_action/', ChangePassword.as_view(), name="change_password_action"),
    path('', include('accounts.EA.ea_urls')),
    path('', include('accounts.St.st_urls')),
    path('', include('accounts.Pr.pr_urls')),
]