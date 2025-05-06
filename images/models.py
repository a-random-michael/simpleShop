from django.db import models
from products.models import Product

class Image(models.Model):
    image = models.ImageField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
#    description = models.TextField(blank=True, null=True)
