from django.db import models
from django.urls import reverse
import random,os
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.utils.encoding import smart_str

def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name,ext = os.path.splitext(base_name)
    return name,ext

def upload_image_path(instance,filename):
    new_filename = random.randint(1,100000000)
    name,ext= get_filename_ext(filename)
    final_filename= f'{new_filename}{ext}'
    return f'products/{new_filename}/{final_filename}'

class Product(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True,editable=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=9999999,decimal_places=2)
    image = models.ImageField(upload_to=upload_image_path)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return smart_str(self.title[:50])
    
    def get_absolute_url(self):
        #return '/products/{slug}/'.format(slug=self.slug)
        return reverse('products:detail',kwargs={'slug':self.slug})
    
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver,sender=Product)

    


