from django.contrib import admin
from django.contrib.admin.sites import site
from products.models import Product

site.register(Product)
# Register your models here.
