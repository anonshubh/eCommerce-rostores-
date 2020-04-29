from django.db import models
from django.urls import reverse
import random,os
from ecommerce_src.utils import unique_slug_generator,get_filename
from django.db.models.signals import pre_save
from django.utils.encoding import smart_str
from django.core.files.storage import FileSystemStorage
from django.conf import settings

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
    price = models.DecimalField(max_digits=100,decimal_places=2)
    image = models.ImageField(upload_to=upload_image_path)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return smart_str(self.title[:50])
    
    def get_absolute_url(self):
        #return '/products/{slug}/'.format(slug=self.slug)
        return reverse('products:detail',kwargs={'slug':self.slug})
    
    @property
    def name(self):
        return self.title
    
    def get_download(self):
        qs = self.productfile_set.all()
        return qs
    
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver,sender=Product)


def upload_product_file_loc(instance,filename):
    slug = instance.product.slug
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = f"products/{slug}/"
    return location + filename

class ProductFile(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length = 128,null=True,blank=True)
    file = models.FileField(upload_to=upload_product_file_loc,storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    free = models.BooleanField(default=False)
    user_required = models.BooleanField(default=False)

    def __str__(self):
        return smart_str(self.file.name)

    def get_download_url(self):
        return reverse('products:download',kwargs={'slug':self.product.slug,'pk':self.pk})
    
    @property
    def display_name(self):
        f_name = get_filename(self.file.name)
        if self.name:
            return self.name
        return f_name
    
    def get_default_url(self):
        return self.product.get_absolute_url()

    


