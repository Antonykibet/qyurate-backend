from django.db import models
from Products.models import Theme
# Create your models here.

class StockImage(models.Model):
    name = models.CharField(max_length=200,null=True,)
    theme = models.ForeignKey(Theme,on_delete=models.PROTECT,
        related_name='stockImages',null=True)
    description = models.TextField(null=True)
    stock_image_url = models.ImageField(upload_to='stockImages/', null=True, blank=True)
