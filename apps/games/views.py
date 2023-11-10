
"""| GAMES VIEW |"""

# Django.
from django.shortcuts import render, redirect
from django.http import Http404, HttpRequest, HttpResponse
from django.views import View
# Rest-framework.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import (
    IsAuthenticated
)
# serializers.
from .serializers import (
    GameSerializer, 
    CreateGameSerializer, 
    SearchRangeProductsSerializer,
    FindPieceSerializer,
    ByDescendingSerializer,
    SubscribeSerializer
)
# models.
from .models import (
    Game,
    UserGame,
    Subscribe
)
from auths.models import CastomUser
# abstracts.
from abstracts.utils import get_object_or_404
from abstracts.mixins import ObjectMixin, ResponseMixin
# utils.
from .utils import (
    save_game_to_user,
    all_user_games
)
# permissions.
from .permissions import GamePermission
# tasks.
from .tasks import (
    do_test,
    game_sub_verifi,
    finish_sub,
    cancel_subcribe
)


class GameViewSet(viewsets.ViewSet, ObjectMixin, ResponseMixin):
    #! для этого надо получить токен
    # permission_classes = (
    #     GamePermission,
    #     IsAuthenticated
    # )
    queryset = Game.objects.all()
    serializer_class = CreateGameSerializer
    
    def list(self, request: Request, *args, **kwargs) -> Response:
        serializer = GameSerializer(instance=self.queryset, many=True)
        return self.json_response(data=serializer.data)
    
    def retrieve(self, request: Request, pk: int = None) -> Response:
        game = self.object_get(self.queryset, pk)
        serializer: GameSerializer = GameSerializer(instance=game)
        return self.json_response(data=serializer.data)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = CreateGameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            game: Game = serializer.save()
            return self.json_response(data=f"Game {game.name} is create! ID: {game.pk}")
        return Response(serializer.errors)
    
    def destroy(self, request: Request, pk: str) -> Response:
        """Удаление игры."""
        game = self.object_get(self.queryset, pk)
        name: str = game.name
        game.delete()
        return self.json_response(data=f"Game {name} deleted! id: {pk}")
    
    def update(self, request: Request, pk: str) -> Response:
        """Обновление игры."""
        data = request.data
        game = self.object_get(self.queryset, pk)
        serializer: GameSerializer = GameSerializer(
            instance=game,
            data=data
        )
        if not serializer.is_valid():
            return self.json_response(status='Warning', data=f'Warning with: {game.name}')
        serializer.save()
        return self.json_response(data=f'Game: {game.name} was updated')
    
    def partial_update(self, request: Request, pk: int) -> Response:
        game = self.object_get(self.queryset, pk)
        serializer: GameSerializer = GameSerializer(
            instance=game,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return self.json_response(status='Warning', data=f'Game: {game.name} was updated')
        serializer.save()
        return self.json_response(data=f'Game: {game.name} was updated')
        
    @action(methods=['POST'], detail=False, url_path='/subscribe/(?P<pk>[^/.]+)')
    def subscribe(self, req: Request, pk:int=None) -> Response:
        CANCEL_TIMEOUT_30_DAYS = 30*24*60*60
        game = self.object_get(queryset=self.queryset, obj_id=pk)
        sub = Subscribe.objects.create(
            user=req.user,
            is_active=True,
            game=game
        )
        cancel_subcribe.apply_async(
            kwargs={'subcribe_id': sub.id},
            countdown=CANCEL_TIMEOUT_30_DAYS
        )
        return self.json_response(
            data={
                "message" : {
                    "game_id": game.id,
                    "subscribe_id": sub.id,
                    "date_finished": sub.datetime_finished
                }
            }
        )

    @action(methods=['GET'], detail=False, url_path='sub/check/(?P<pk>[^/.]+)')
    def subscribe_check(self, req: Request, pk:int=None) -> Response:
        context:dict = {}
        context['game_id'] = pk
        game_sub_verifi.apply_async(kwargs=context,countdown=30*24*60*60)
        return self.json_response(
            data={"massage" : "ok"}
        )
        
    @action(methods=['POST'], detail=False, url_path='sub/finish/(?P<pk>[^/.]+)')
    def buy_subscribe(self, req: Request, pk:int=None) -> Response:
        context:dict = {}
        CANCEL_TIMEOUT_30_DAYS = 30*24*60*60
        Subscribe = Subscribe.objects.create(
            game=Game.objects.get(id=pk),
            user=req.user,
            is_active=True,
            auto_buy=...            
        )
        context['sub'] = Subscribe
        game_sub_verifi.apply_async(kwargs=context,countdown=CANCEL_TIMEOUT_30_DAYS)
        return self.json_response(
            data={"massage" : "[OK] Sub is False"}
        )
    

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

class SubscribeViewSet(viewsets.ViewSet):
    queryset = Subscribe.objects.filter(is_active=True)
    serializer_class = SubscribeSerializer

    def list(self, req: Request, *args, **kwargs) -> Response:
        serializer = SubscribeSerializer(instance=self.queryset, many=True)
        return Response(data=serializer.data)

    def create(self, req: Request, *args, **kwargs) -> Response:
        serializer = SubscribeSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            sub: Subscribe = serializer.save()
            finish_sub.apply_async(kwargs={"sub": sub},countdown=30*24*60*60)
        return Response(serializer.errors)