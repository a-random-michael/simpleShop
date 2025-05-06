from django.db import models


class Tags(models.Model):
    title = models.CharField(max_length=150)
    #created = models.DateTimeField(auto_now_add=True)
    #modified = models.DateTimeField(auto_now=True)


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField(default=0)
    #created = models.DateTimeField(auto_now_add=True)
    #modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tags)
    thumbnail = models.ImageField(blank=True, default='default.png')
    # TODO: Should be added:
    # price
    # catalog (for discription images)
