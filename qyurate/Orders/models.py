import uuid
from django.db import models
from Products.models import Product
from business_partner.models import Shop
from common.constants import ORDER_STATUS, NOTIFICATION_METHODS, ORDER_MSG_DELIVERY_STATUS

class Order(models.Model):
    guid = models.UUIDField(auto_created=True,default=uuid.uuid4,unique=True, null=False, blank=False, editable=False)
    # TODO: configure a robust random code generator
    code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=200,null=True)
    customer_email = models.EmailField(null=True)
    customer_phone_no = models.CharField(max_length=20,null=True)
    address = models.TextField(null=True)
    extra_info = models.TextField(null=True, blank=True)
    status = models.CharField(choices=ORDER_STATUS, max_length=50, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        items = self.order_items.all()
        return sum([item.price * item.quantity for item in items])

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        # late import to avoid circular imports
        from Orders.helpers import generate_order_code
        if not self.code:
            self.code = generate_order_code()
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    submitted_design = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(null=True)

class OrderNotificationLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    notification_method = models.CharField(choices=NOTIFICATION_METHODS, max_length=50)
    contact_info = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_MSG_DELIVERY_STATUS, default='PENDING')
    error_message = models.TextField(null=True, blank=True)