# Django.
from django.shortcuts import render
# rest_framework.
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from abstracts.mixins import ResponseMixin
# serializers.
from .serializers import (
    CreateUserSerializer, 
    UserSerializer
)
# models.
from .models import CastomUser
from auths.paginators import MyLimitPaginator

class UserViewSet(viewsets.ViewSet, ResponseMixin):
    queryset = CastomUser.objects.all()
    serializer_class = CreateUserSerializer
    pagination_class = MyLimitPaginator
    
    def list(self, req: Request, *args, **kwargs) -> Response:
        queryset = self.queryset
        paginator = MyLimitPaginator()
        page = paginator.paginate_queryset(queryset, req)
        serializer = UserSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def create(self, req: Request, *args, **kwargs) -> Response:
        def default_name(user_id: int):
            return f"user{user_id}"
        serializer = CreateUserSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            pas1 = serializer.validated_data['password']
            pas2 = serializer.validated_data['repeat_password']
            if pas1 == pas2:
                user: CastomUser = \
                    CastomUser.objects.create_user(
                    email=serializer.validated_data['email'],
                )
                user.set_password(pas1)
                user.name = default_name(user.id)
                user.save()
                return self.json_response(data=f"User {user.email} is create! ID: {user.pk}")
            else:
                return self.json_response(status='Warning', data=f'{pas1} != {pas2}')
        return Response(serializer.errors)
            
            
