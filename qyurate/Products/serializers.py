from Products.models import Theme, Product
from rest_framework import serializers

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = "__all__" 
        
class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'thumbnail_image_url', 'price')


class ProductSerializer(serializers.ModelSerializer):
    theme_details = ThemeSerializer(read_only=True, source='theme')
    base_product_details = BaseProductSerializer(read_only=True, source='base_product')

    class Meta:
        model = Product
        fields = "__all__"

