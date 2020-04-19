from django.shortcuts import render,get_object_or_404
from .models import Product

def products_list(request):
    context={
        'object_list':Product.objects.all()
    }
    return render(request,'products/products_list.html',context)

def product_detail(request,slug):
    context={
        'product':get_object_or_404(Product,slug=slug)
    }
    return render(request,'products/product_detail.html',context)


