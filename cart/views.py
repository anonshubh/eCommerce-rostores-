from django.shortcuts import render,redirect
from .models import Cart
from products.models import Product

def cart_home(request):
    cart_obj,new_obj= Cart.objects.get_or_new(request)
    return render(request,"cart/home.html",{'cart':cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.filter(id=product_id).first()
        except Product.DoesNotExist:
            return redirect('cart:home')
        cart_obj,new_obj = Cart.objects.get_or_new(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart:home')


