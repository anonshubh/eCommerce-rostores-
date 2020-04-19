from django.db import models
from products.models import Product

class Tag(models.Model):
    title = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product,blank=True)

    def __str__(self):
        return self.title[:25]
    