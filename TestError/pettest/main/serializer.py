from .models import Pet
from rest_framework import serializers
from .models import MyUserManager

from django.contrib.auth.models import User

from .models import UserProfile


class PetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('id', 'vin', 'user')


class PetDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Pet
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'password', 'password2')
