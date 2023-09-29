
"""| GAMES VIEW |"""

# Django.
from django.shortcuts import render, redirect
from django.http import Http404, HttpRequest, HttpResponse
from django.views import View
# Rest-framework.
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import ValidationError
# serializers.
from .serializers import GameSerializer, CreateGameSerializer
# Models.
from .models import Game
from auths.models import CastomUser
# Local.
from abstracts.utils import get_object_or_404


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

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = CreateGameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            game: Game = serializer.save()
            return Response(data={
                'status': 'OK',
                'message': f"Game {game.name} is create! ID: {game.pk}"
                }
            )
        return Response(serializer.errors)


class ActiveGameViewSer(viewsets.ViewSet):
    queryset = Game.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        active_games: list = [game for game in self.queryset if game.is_active]
        serializer = GameSerializer(instance=active_games, many=True)
        return Response(data=serializer.data)


class BuyGameView(View):
    template: str = '' 
    def get(self, request: HttpRequest, game_id: int) -> HttpResponse:
        user: CastomUser = request.user
        game: Game =  get_object_or_404(Game, game_id, 'Игра не найдена')
        if game.is_active == False:
            return HttpResponse('Игры нет в наличии')
        context: dict = {}
        context['game'] = game
        return render(request, self.template, context)

    def post(self, request: HttpRequest, game_id: int) -> HttpResponse:
        user: CastomUser = request.user
        data = request.POST
        game: Game =  get_object_or_404(Game, game_id)

        if user.balance >= game.price:
            user.balance -= game.price
            user.save()
            game.user = user
            game.quantity -= 1
            game.save()
            # return redirect()
        else: return Http404("...")
