from django.db import models
from common.constants import NOTIFICATION_METHODS

class Shop(models.Model):
    name = models.CharField(max_length=255)
    # TODO: impose a unique constraint on url and domain
    url = models.URLField(blank=True,null=True, unique=True)
    domain = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=False, null=False)
    phone_contact = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name

class SiteConfigs(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='site_configs')
    logo_url = models.URLField(blank=True, null=True)
    color_palette = models.CharField(max_length=7, default="#FF6A07")  # Hex color code
    hero_image_url = models.URLField(blank=True, null=True)
    hero_text = models.CharField(max_length=255, blank=True, null=True)
    notification_method = models.CharField(max_length=50, choices=NOTIFICATION_METHODS)