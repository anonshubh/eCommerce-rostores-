from django.shortcuts import render,redirect
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm,GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressCheckoutForm
from addresses.models import Address
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template

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
            product_added = False
        else:
            cart_obj.products.add(product_obj)
            product_added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            json_data={
                'added': product_added,
                'removed': not product_added,
                'count': cart_obj.products.count(),
            }
            return JsonResponse(json_data)
    return redirect('cart:home')

def checkout_home(request):
    cart_obj,new_obj= Cart.objects.get_or_new(request)
    order_obj=None
    if new_obj or cart_obj.products.count() == 0:
        return redirect('cart:home')
    form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressCheckoutForm()
    billing_address_id = request.session.get('billing_address_id',None)

    shipping_address_required = not cart_obj.is_digital

    shipping_address_id = request.session.get('shipping_address_id',None)
    billing_profile,billing_profile_created = BillingProfile.objects.get_or_new(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj ,new_order_obj = Order.objects.get_or_new(billing_profile,cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            if request.session['shipping_address_id']:
                del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            if request.session['billing_address_id']:
                del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            del request.session['cart_items']
            request.session['order_ref']= order_obj.order_id
            user_email = order_obj.billing_profile.user.email
            cxt = {'order_id':order_obj.order_id}
            txt_ = get_template('cart/email/order.txt').render(cxt)
            html_ = get_template('cart/email/order.html').render(cxt)
            subject = "Purchase Successful"     
            send_mail(subject,txt_,settings.DEFAULT_FROM_EMAIL,[user_email],html_message=html_,fail_silently=False)
            return redirect('cart:success')
    context={
        'order':order_obj,
        'billing_profile':billing_profile,
        'form':form,
        'guest_form':guest_form,
        'address_form':address_form,
        'address_qs':address_qs,
        'shipping_address_required':shipping_address_required,
    }
    return render(request,'cart/checkout.html',context)


def checkout_done_view(request):
    ref = None
    if request.session['order_ref']:
        ref = request.session['order_ref']

    return render(request,'cart/checkout_done.html',{'ref':ref})

