from rest_framework import serializers
from canvas.models import StockImage

class StockImageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = StockImage
        fields = '__all__' 