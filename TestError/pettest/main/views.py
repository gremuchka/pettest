from Tools.scripts.mkreal import join
from django.shortcuts import render
from rest_framework import generics
from .serializer import PetDetailSerializer, PetListSerializer, UserRegistrationSerializer, UserDetailSerializer
from .models import Pet, UserProfile
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from rest_framework.response import Response
from rest_framework import status

from knox.models import AuthToken

from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


class PetCreateView(generics.CreateAPIView):
    serializer_class = PetDetailSerializer


class PetListView(generics.ListAPIView):
    serializer_class = PetListSerializer
    queryset = Pet.objects.all()
    permission_classes = (IsAdminUser,)


class PetDetailViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetDetailSerializer
    queryset = Pet.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)


class UserRegistrationView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
