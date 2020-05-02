from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order,ProductPurchase
from billing.models import BillingProfile
from django.http import Http404

class OrderListView(LoginRequiredMixin,ListView):

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()

class OrderDetailView(LoginRequiredMixin,DetailView):
    context_object = 'order'

    def get_object(self):
        qs = Order.objects.by_request(self.request).filter(order_id = self.kwargs.get("order_id"))
        if qs.count() == 1:
            return qs.first()
        raise Http404

class LibraryView(LoginRequiredMixin,ListView):
    template_name = 'orders/library.html'
    def get_queryset(self):
        return ProductPurchase.objects.products_by_request(self.request)
    

def cancel_order(request,**kwargs):
    order_id = kwargs.get('order_id')
    obj = Order.objects.get(order_id=order_id)
    context = {'order':obj.order_id}
    if request.method == 'POST':    
        obj.cancellation()
        return redirect('orders:list')
    return render(request,'orders/cancel.html',context)
    


    
