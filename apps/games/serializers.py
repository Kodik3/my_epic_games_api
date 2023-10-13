# Rest_framework.
from rest_framework import serializers
# models.
from .models import Game


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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.poster = validated_data.get('poster', instance.poster)
        instance.save()
        return instance
    
    
class CreateGameSerializer(serializers.ModelSerializer):
    rate= serializers.FloatField(default=0)
    quantity= serializers.IntegerField(default=0)
    class Meta:
        model = Game
        fields = ['name', 'price', 'poster', 'rate', 'quantity']

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

