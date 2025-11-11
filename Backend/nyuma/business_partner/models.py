from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=255)
    # TODO: impose a unique constraint on url
    url = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name

class SiteConfigs(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='site_configs')
    logo_url = models.URLField(blank=True, null=True)
    color_palette = models.CharField(max_length=7, default='#FFFFFF')  # Hex color code
    hero_image_url = models.URLField(blank=True, null=True)
    hero_text = models.CharField(max_length=255, blank=True, null=True)