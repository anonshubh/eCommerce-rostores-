from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from .forms import LoginForm,RegisterForm,GuestForm
from django.utils.http import is_safe_url
from .models import GuestEmail
from django.views.generic import CreateView

User = get_user_model()

def login_page(request):
    form = LoginForm(request.POST or None)
    redirect_path = request.GET.get('next') or request.POST.get('next_post') or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            return redirect('home')
    return render(request,'login.html',{'form':form})

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'

def guest_register_page(request):
    form = GuestForm(request.POST or None)
    redirect_path = request.GET.get('next') or request.POST.get('next_post') or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        return redirect('accounts:register_url')
    return redirect('accounts:register_url')


