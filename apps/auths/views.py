from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateUserSerializer, UserSerializer
from .models import CastomUser
from abstracts.mixins import ResponseMixin


class AuthUserViewSet(viewsets.ViewSet, ResponseMixin):
    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, req: Request, *args, **kwargs) -> Response:
        serializer = CreateUserSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            pas1 = serializer.validated_data['password']
            pas2 = serializer.validated_data['password2']
            if pas1 == pas2:
                user: CastomUser = \
                    CastomUser.objects.create_user(
                    email=serializer.validated_data['email'],
                    password=pas1
                )
                return self.json_response(data=f"User {user.email} is create! ID: {user.pk}")
            else:
                return self.json_response(status='Warning', data=f'{pas1} != {pas2}')
        return Response(serializer.errors)
            
            
