from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,ProductFile
from cart.models import Cart
from analytics.signals import object_viewed_signal
from django.views.generic import ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from wsgiref.util import FileWrapper
from django.conf import settings
import os
from mimetypes import guess_type
from orders.models import ProductPurchase
from django.contrib import messages

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

class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not found")
        download_obj = downloads_qs.first()
        can_download = False
        user_ready  = True
        if download_obj.user_required:
            if not request.user.is_authenticated:
                user_ready = False
        purchased_products = Product.objects.none()
        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to download this item")
            return redirect(download_obj.get_default_url())
        file_root = settings.PROTECTED_ROOT
        filepath = download_obj.file.path # .url /media/
        final_filepath = os.path.join(file_root, filepath) # where the file is stored
        with open(final_filepath, 'rb') as f:
            wrapper = FileWrapper(f)
            mimetype = 'application/force-download'
            gussed_mimetype = guess_type(filepath)[0] # filename.mp4
            if gussed_mimetype:
                mimetype = gussed_mimetype
            response = HttpResponse(wrapper, content_type=mimetype)
            response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.name)
            response["X-SendFile"] = str(download_obj.name)
            return response




