from rest_framework import serializers
from .models import CastomUser



class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    repeat_password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastomUser
        fields = ['email', 'name', 'password']