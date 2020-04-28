from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from .forms import LoginForm,RegisterForm,GuestForm,ReactivateEmailForm
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from .models import GuestEmail,EmailActivation
from django.views.generic import CreateView,DetailView,View,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.db.models import Q
from .mixins import NextUrlMixin,RequestFormAttachMixin
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/login.html'
    default_next = 'home'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class RegisterView(SuccessMessageMixin,CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login_url')
    success_message = "Verification mail has been sent to your Email."

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

class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user


class AccountEmailActivateView(FormMixin,View):
    success_url = reverse_lazy('accounts:login_url')
    form_class = ReactivateEmailForm
    key = None
    def get(self,request,key=None,*args,**kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count()==1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request,"Your Email has been confirmed, Please login.")
                return redirect('accounts:login_url')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your Email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?""".format(link=reset_link)
                    messages.success(request,mark_safe(msg))
                    return redirect('accounts:login_url')
        return render(request,'registration/activation-error.html',{'form':self.get_form(),'key':key})

    def post(self,request,*args,**kwagrs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return  self.form_invalid(form)
    
    def form_valid(self, form):
        msg = """Activation Link Sent, please check your Email."""
        messages.success(self.request,msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.filter(Q(email=email) | Q(user__email=email)).filter(activated=False).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user,email=email)
        new_activation.send_activation_email()
        return super(AccountEmailActivateView,self).form_valid(form)

    def form_invalid(self, form):
        return render(self.request,'registration/activation-error.html',{'form':form,"key":self.key})
