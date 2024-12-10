from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=256)
    restaurant_name = serializers.CharField(max_length=256)
    quantity = serializers.IntegerField()

class DummySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField(max_length=256)
    products = serializers.ListField(child=ProductSerializer())