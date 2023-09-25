from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=11, decimal_places=2)
    poster = serializers.ImageField()
    quantity = serializers.IntegerField()
    
    
class CreateGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['name', 'price', 'poster', 'rate', 'quantity']