
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
from .serializers import (
    GameSerializer, 
    CreateGameSerializer, 
    SearchRangeProductsSerializer,
    FindPieceSerializer,
    ByDescendingSerializer
)
# Models.
from .models import (
    Game, 
    UserGame
)
from auths.models import CastomUser
# Local.
from abstracts.utils import get_object_or_404
from .utils import (
    save_game_to_user,
    all_user_games
)



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
        serializer: GameSerializer = GameSerializer(instance=game)
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
    
    def destroy(self, request: Request, pk: str) -> Response:
        """Удаление игры."""
        try:
            game: Game = self.queryset.get(id=pk)
        except Game.DoesNotExist:
            raise ValidationError('Game not found!', code=404)
        name: str = game.name
        game.delete()
        return Response(
            data={
                'status': 'OK',
                'message': f"Game {name} deleted! id: {pk}"
            }
        )
    
    def update(self, request: Request, pk: str) -> Response:
        """Обновление игры."""
        try:
            game = self.queryset.get(id=pk)
        except Game.DoesNotExist:
            raise ValidationError('Game not found', code=400)

        serializer: GameSerializer = GameSerializer(
            instance=game,
            data=request.data
            )
        if not serializer.is_valid():
            return Response(
                data={
                    'status': 'Warning',
                    'message': f'Warning with: {game.name}'
                }
            )
        serializer.save()
        return Response(
            data={
                'status': 'OK',
                'message': f'Game: {game.name} was updated'
            }
        )
    
    def partial_update(self, request: Request, pk: int) -> Response:
        try:
            game = self.queryset.get(id=pk)
        except Game.DoesNotExist:
            raise ValidationError('Game not found', code=400)

        serializer: GameSerializer = GameSerializer(
            instance=game,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(
                data={
                    'status': 'Warning',
                    'message': f'Warning with: {game.name}'
                }
            )

        serializer.save()
        return Response(data={
            'status': 'OK',
            'message': f'Game: {game.name} was updated'
        })
    

class ActiveGameViewSet(viewsets.ViewSet):
    queryset = Game.objects.filter(quantity__gt=0)
    serializer_class = GameSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        serializer = GameSerializer(instance=self.queryset, many=True)
        return Response(data=serializer.data)


class BuyGameView(View):
    template: str = ''
    
    def get(self, request: HttpRequest, game_id: int) -> HttpResponse:
        context: dict = {}
        user: CastomUser = request.user
        game: Game =  get_object_or_404(Game, game_id, 'Игра не найдена')
        if game.is_active == False:
            return HttpResponse('Игры нет в наличии')
        context['game'] = game
        return render(request, self.template, context)

    def post(self, request: HttpRequest, game_id: int) -> HttpResponse:
        user: CastomUser = request.user
        game: Game = get_object_or_404(Game, game_id)
        
        user_games = UserGame.objects.filter(user=user, game=game)

        if user_games.exists():
            return Response("У вас есть эта игра")
        if user.balance >= game.price:
            save_game_to_user(game=game, user=user)
            # TODO: перекинть на страицу игры
        else:
            return Response("Не хватате средств!")


class SearchProductsInPriceRange(viewsets.ViewSet):
    """ Поиск товаров в ценовом диапазоне """
    serializer_class = SearchRangeProductsSerializer

    def get_queryset(self, x, y):
        return Game.objects.filter(price__range=(x, y))

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = SearchRangeProductsSerializer(data=request.data)
        if serializer.is_valid():
            price1 = serializer.validated_data['price1']
            price2 = serializer.validated_data['price2']
            queryset = self.get_queryset(price1, price2)
            serializer = GameSerializer(instance=queryset, many=True)
            return Response(data=serializer.data)
        return Response(serializer.errors)


class FindPieceOfTextViewSet(viewsets.ViewSet):
    """ Поиск товаров по части слова """
    serializer_class = FindPieceSerializer

    def get_queryset(self, piece: str):
        return Game.objects.filter(name__icontains=f"{piece}")

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = FindPieceSerializer(data=request.data)
        if serializer.is_valid():
            piece = serializer.validated_data['name']
            queryset = self.get_queryset(str(piece))
            serializer = GameSerializer(instance=queryset, many=True)
            return Response(data=serializer.data)
        return Response(serializer.errors)
    

class ByDescendingViewSet(viewsets.ViewSet):
    """ Поиск товаров по цене убывания, возрастания """
    serializer_class = ByDescendingSerializer

    def get_queryset(self, value, choise):
        if value is True:
            return Game.objects.all().order_by(f'-{choise}')
        else:
            return Game.objects.all().order_by(f'{choise}')

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = ByDescendingSerializer(data=request.data)
        if serializer.is_valid():
            value = serializer.validated_data['descending']
            choise = serializer.validated_data['choises']
            queryset = self.get_queryset(value, choise)
            serializer = GameSerializer(instance=queryset, many=True)
            return Response(data=serializer.data)
        return Response(serializer.errors)