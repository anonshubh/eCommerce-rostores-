from django.shortcuts import render,get_object_or_404
from .models import Product
from cart.models import Cart
from analytics.signals import object_viewed_signal
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


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

class UserProductHistoryView(LoginRequiredMixin,ListView):
    template_name = 'products/user_history.html'

    def get_context_data(self, *args, **kwargs):
        context =  super(UserProductHistoryView,self).get_context_data(*args,**kwargs)
        cart_obj,new_obj = Cart.objects.get_or_new(self.request)
        context['cart'] = cart_obj
        return context
    
    def get_queryset(self):
        request = self.request
        views = request.user.objectviewed_set.all().by_model(Product)
        viewed_ids = [x.object_id for x in views]
        return Product.objects.filter(pk__in =viewed_ids)




