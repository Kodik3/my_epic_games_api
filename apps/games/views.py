
"""| GAMES VIEW |"""

# Django.
from django.shortcuts import render
from django.http import Http404
# Rest-fremework.
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import ValidationError
# serializers.
from .serializers import GameSerializer, CreateGameSerializer
# Models.
from .models import Game


class GameViewSet(viewsets.ViewSet):
    queryset = Game.objects.all()
    serializer_class = CreateGameSerializer
    
    def list(self, request: Request, *args, **kwargs) -> Response:
        serializer = GameSerializer(instance=self.queryset, many=True)
        return Response(data=serializer.data)
    
    def retrieve(self, request: Request, pk: int = None) -> Response:
        try:
            game = self.queryset.get(id=pk)
        except Game.DoesNotExist:
            raise ValidationError('Игра не найдена', code=404)
        serializer = GameSerializer(instance=game)
        return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ActiveGameViewSer(viewsets.ViewSet):
    queryset = Game.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        active_games: list = [game for game in self.queryset if game.is_active]
        serializer = GameSerializer(instance=active_games, many=True)
        return Response(data=serializer.data)
