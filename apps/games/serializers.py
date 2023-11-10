# Rest_framework.
from rest_framework import serializers
# models.
from .models import (
    Game,
    GameComment,
    Subscribe
)


class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=11,
        decimal_places=2,
        required=False
    )
    poster = serializers.ImageField(required=False)
    rate = serializers.FloatField(required=False)
    is_active = serializers.BooleanField()
    is_discount = serializers.BooleanField(required=False)
    discount = serializers.FloatField(required=False)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.poster = validated_data.get('poster', instance.poster)
        
        instance.is_discount = validated_data.get('is_discount', instance.is_discount)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance
    
    
class CreateGameSerializer(serializers.ModelSerializer):
    rate= serializers.FloatField(default=0, required=False)
    quantity= serializers.IntegerField(default=0, required=False)
    is_discount = serializers.BooleanField(required=False)
    discount = serializers.FloatField(required=False)
    class Meta:
        model = Game
        fields = ['name', 'price', 'poster', 'rate', 'quantity', 'is_discount', 'discount']


class SearchRangeProductsSerializer(serializers.Serializer):
    price1 = serializers.DecimalField(max_digits=11, decimal_places=2)
    price2 = serializers.DecimalField(max_digits=11, decimal_places=2)


class FindPieceSerializer(serializers.Serializer):
    name = serializers.CharField()


class ByDescendingSerializer(serializers.Serializer):
    choises = serializers.ChoiceField(
        choices= (
            ('id', 'ID'),
            ('rate' , 'Rate'),
            ('price', 'Price'),
            ('quantity', 'Quantity')
        )
    )
    descending = serializers.BooleanField(default=False)
    

class GameCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameComment
        fields = ['user', 'game', 'text']


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['game', 'user']
