from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.serializers import (
    CustomTokenObtainSerializer,
    ProfileSerializer,
    RegistrationSerializer,
)

__all__ = ['CustomTokenObtainView', 'RegistrationView', 'ProfileView']


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class RegistrationView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)


class ProfileView(SerializerExtensionsAPIViewMixin, generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
