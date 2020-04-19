from django.db import models
from products.models import Product
from django.utils.encoding import smart_str

class Tag(models.Model):
    title = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product,blank=True)

    def __str__(self):
        return smart_str(self.title[:25])
    