from django.db import models
from business_partner.models import Shop

class User(models.Model):
    username = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    def __str__(self):
        return self.username
