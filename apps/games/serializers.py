# Rest_framework.
from rest_framework import serializers
# models.
from .models import Game


class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=11, decimal_places=2)
    poster = serializers.ImageField()
    rate = serializers.FloatField()
    quantity = serializers.IntegerField()
    
    
class CreateGameSerializer(serializers.ModelSerializer):
    rate= serializers.FloatField(default=0)
    quantity= serializers.IntegerField(default=0)
    class Meta:
        model = Game
        fields = ['name', 'price', 'poster', 'rate', 'quantity']