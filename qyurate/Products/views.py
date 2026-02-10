from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from Products.models import Theme, Product
from Products.serializers import ProductSerializer, ThemeSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']
    

class ProductViewSet(viewsets.ModelViewSet):
    """Handles both regular products and templates. Use `is_template` filter to select templates."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['name','description']
    filterset_fields = ['is_template', 'theme__type', 'theme__name', 'base_product__name']
    