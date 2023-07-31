from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price', 'product_tax', 'inventory', 'collection']

    product_tax = serializers.SerializerMethodField('calculating_tax')

    def calculating_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)