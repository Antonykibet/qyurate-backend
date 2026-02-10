from django.db import models
from django.contrib.auth.models import AbstractUser
from business_partner.models import Shop

class QyurateUser(AbstractUser):
    address = models.TextField(blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
