from rest_framework import serializers
from .models import CastomUser



class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastomUser
        fields = ['email', 'password', 'password2']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastomUser
        fields = ['email', 'nickname', 'password']