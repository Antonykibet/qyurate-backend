from rest_framework import serializers
from business_partner.models import Shop, SiteConfigs

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__" 

class SiteConfigsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfigs
        fields = "__all__"