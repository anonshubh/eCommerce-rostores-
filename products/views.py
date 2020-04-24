from django.shortcuts import render,get_object_or_404
from .models import Product
from cart.models import Cart
from analytics.signals import object_viewed_signal


def products_list(request):
    context={
        'object_list':Product.objects.all()
    }
    return render(request,'products/products_list.html',context)

def product_detail(request,slug):
    cart_obj,new_obj = Cart.objects.get_or_new(request)
    obj = get_object_or_404(Product,slug=slug)
    object_viewed_signal.send(obj.__class__,instance=obj,request=request)
    context={
        'product':obj,
        'cart':cart_obj
    }
    return render(request,'products/product_detail.html',context)




