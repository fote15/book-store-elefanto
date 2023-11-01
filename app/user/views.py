"""
Views for the user API
"""
from rest_framework import generics
from rest_framework.serializers import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework import authentication, permissions


class CreateUserView(generics.CreateAPIView):
    """Create a new user """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """return atuhed user"""
        return self.request.user
