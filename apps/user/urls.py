from django.urls import re_path
from rest_framework_simplejwt.views import token_refresh, token_verify

from apps.user.views import (
    CustomTokenObtainView,
    ProfileView,
    RegistrationView,
)

urlpatterns = [
    re_path(r'^api/v1/registration/$', RegistrationView.as_view(), name='registration'),
    re_path(r'^api/v1/token/$', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/v1/token/refresh/$', token_refresh, name='token_refresh'),
    re_path(r'^api/v1/token/verify/$', token_verify, name='token_verify'),
    re_path(r'^api/v1/profile/', ProfileView.as_view(), name='profile'),
]
