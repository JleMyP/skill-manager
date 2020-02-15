"""hack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import re_path
from rest_framework_simplejwt.views import token_refresh, token_verify

from .views import CustomTokenObtainView
from .views import ProfileView
from .views import RegistrationView

urlpatterns = [
    re_path(r'^api/v1/registration/$', RegistrationView.as_view(), name='registration'),
    re_path(r'^api/v1/token/$', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/v1/token/refresh/$', token_refresh, name='token_refresh'),
    re_path(r'^api/v1/token/verify/$', token_verify, name='token_verify'),
    re_path(r'^api/v1/profile/', ProfileView.as_view(), name='profile'),
]
