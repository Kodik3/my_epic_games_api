# Django.
from django.shortcuts import render
# rest_framework.
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
# mixins.
from abstracts.mixins import ResponseMixin
# serializers.
from .serializers import (
    CreateUserSerializer, 
    UserSerializer
)
# models.
from .models import CastomUser
from auths.paginators import (
    UserPageNumberPaginator,
    UserLimitOffsetPaginator,
)

class UserViewSet(viewsets.ViewSet, ResponseMixin):
    queryset = CastomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPageNumberPaginator

    @action(methods=['get'], detail=False, url_path='paginator-page-number', permission_classes=(AllowAny,))
    def paginator_page_number(self, req: Request) -> Response:
        paginator: UserPageNumberPaginator = self.pagination_class()
        objects: list = paginator.paginate_queryset(self.queryset, req)
        serializer: UserSerializer = UserSerializer(objects, many=True)
        return self.json_response(serializer.data, paginator=paginator)
    
    @action(methods=['get'], detail=False, url_path='paginator-limit-offset', permission_classes=(AllowAny,))
    def paginator_limit_offset(self, req: Request) -> Response:
        paginator: UserLimitOffsetPaginator = UserLimitOffsetPaginator()
        objects: list = paginator.paginate_queryset(self.queryset,req)
        serializer: UserSerializer = UserSerializer(objects, many=True)
        return self.json_response(serializer.data, paginator=paginator)


                
