from django.db import models
from django.utils.text import slugify

# Create your models here.

class Theme(models.Model):
    theme_types = {
        'RANDOM THEME':'Random theme',
        'GIFT THEME':'Gift theme',
    }
    name = models.CharField(max_length=200,null=True)
    type = models.CharField(choices=theme_types,max_length=200,) 

class Product(models.Model):
    name = models.CharField(max_length=200,null=True,)
    slug = models.SlugField(max_length=250, blank=True)
    thumbnail_image_url = models.ImageField(upload_to='products/', null=True, blank=True)
    base_image_url = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.IntegerField(null=True)
    description = models.TextField(null=True,blank=True)
    # Template-related fields (merged Template into Product)
    is_template = models.BooleanField(default=False)
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT,
        related_name='products', null=True, blank=True)
    base_product = models.ForeignKey('self', on_delete=models.PROTECT,
        related_name='themed_products', null=True, blank=True)
    template_description = models.TextField(null=True,blank=True)
    canvasJSON = models.JSONField(null=True, blank=True)
    canvasSVG = models.TextField(null=True, blank=True)
    canvasPNG = models.TextField(null=True, blank=True)
    likes = models.IntegerField(default=0)
    clicked = models.IntegerField(default=0)

    def populate_is_template(self):
        """Sets the is_template flag based on whether theme and base_product are set."""
        if self.theme and self.base_product:
            self.is_template = True
        else:
            self.is_template = False

    def save(self, *args, **kwargs):
        self.populate_is_template()
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
