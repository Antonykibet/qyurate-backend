from rest_framework import viewsets, response, filters
from django_filters.rest_framework import DjangoFilterBackend
from Orders.models import Order
from Orders.serializers import OrderSerializer, OrderItemSerializer
from Orders.helpers import prepare_order_notification, send_order_notification
from business_partner.utils import get_shop

import logging

LOGGER = logging.getLogger(__name__)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['code','customer_name','customer_email']
    filterset_fields = ['status']

    def create(self, request, *args, **kwargs):
        try:
            customer_info = request.data.get('customer',{})
            cart_items = request.data.get('cart',{})
            shop = get_shop(request)
            order_data = {**customer_info, 'shop': shop.id}
            order_serializer = self.serializer_class(data=order_data)
            order_serializer.is_valid(raise_exception=True)
            order = order_serializer.save()

            for item in cart_items:
                item_data = {**item, 'order': order.id}
                order_item_serializer = OrderItemSerializer(data=item_data)
                order_item_serializer.is_valid(raise_exception=True)
                order_item_serializer.save()

            prepare_order_notification(order, shop)
            # first attempt to send the notification
            send_order_notification(order)
            return response.Response(self.serializer_class(order).data, status=201)
        except Exception as e:
            LOGGER.error('Failed to create order', exc_info=True)
            return response.Response({'error': str(e)}, status=400)
