from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct
from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError("Название продукта должно содержать не менее 5 символов.")
        return value


class ProductPositionSerializer(serializers.ModelSerializer):
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all(), required=False)
    product_name = serializers.SerializerMethodField()
    product_description = serializers.SerializerMethodField()

    class Meta:
        model = StockProduct
        fields = ['product', 'product_name', 'product_description', 'quantity', 'price', 'stock']


    def get_product_name(self, obj):
        return obj.product.title


    def get_product_description(self, obj):
        return obj.product.description



class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        for position_data in positions_data:
            product = position_data.pop('product')
            quantity = position_data.pop('quantity')
            price = position_data.pop('price')
            StockProduct.objects.update_or_create(stock=stock, product_id=product.id,
                                                  defaults={'quantity': quantity, 'price': price})
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        for position_data in positions_data:
            product = position_data.pop('product')
            quantity = position_data.pop('quantity')
            price = position_data.pop('price')
            StockProduct.objects.update_or_create(stock=instance, product_id=product.id,
                                                  defaults={'quantity': quantity, 'price': price})

        return instance
