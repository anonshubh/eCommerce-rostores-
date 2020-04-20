from django.shortcuts import render,get_object_or_404
from .models import Product
from cart.models import Cart

def products_list(request):
    context={
        'object_list':Product.objects.all()
    }
    return render(request,'products/products_list.html',context)

def product_detail(request,slug):
    cart_obj,new_obj = Cart.objects.get_or_new(request)
    context={
        'product':get_object_or_404(Product,slug=slug),
        'cart':cart_obj
    }
    return render(request,'products/product_detail.html',context)


