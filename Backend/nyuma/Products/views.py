from rest_framework import permissions, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from Products.models import ThemedProduct, Theme, AvailableProducts
from Products.serializers import ProductSerializer, ThemeSerializer, AvailableItemSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ThemedProduct.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['theme__type', 'theme__name','base_product__name']


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']
    
class AvailableItemViewSet(viewsets.ModelViewSet):
    queryset = AvailableProducts.objects.all()
    serializer_class = AvailableItemSerializer
    