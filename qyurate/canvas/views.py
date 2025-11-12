from django.shortcuts import render
from rest_framework import permissions, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from canvas.models import StockImage
from canvas.serializers import StockImageSerializer
# Create your views here.

class StockImageViewSet(viewsets.ModelViewSet):
    queryset = StockImage.objects.all()
    serializer_class = StockImageSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['name','description']
    filterset_fields = ['theme__type', 'theme__name']