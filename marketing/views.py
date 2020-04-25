from django.shortcuts import render,redirect
from django.views.generic import UpdateView,View
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import MarketingPreference
from .forms import MarketingPreferenceForm
from .utils import Mailchimp

MAILCHIMP_EMAIL_LIST_ID = getattr(settings,'MAILCHIMP_EMAIL_LIST_ID',None)

class MarketingPreferenceUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    login = 'login_url'
    form_class = MarketingPreferenceForm
    template_name = 'marketing/form.html'
    success_url = reverse_lazy('marketing:opt_email')
    success_message = "Your email preferences has been Updated, Thank You!"

    def get_object(self):
        user = self.request.user
        obj,created = MarketingPreference.objects.get_or_create(user)
        return obj

class MailchimpWebhookView(View):
    def post(self,request,*args,**kwagrs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            email = data.get('data[email]')
            hook_type = data.get('type')
            response_status,response = Mailchimp().check_subscription_status(email)
            sub_status = response['status']
            is_sub = None
            mailchimp_sub = None
            if sub_status == "subscribed":
                is_sub,mailchimp_sub = (True,True)
            elif sub_status == "unsubscribed":
                is_sub,mailchimp_sub = (False,False)
            if is_sub is not None and mailchimp_sub is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_sub,mailchimp_subscribed=mailchimp_sub,mailchimp_msg=str(data))

            return HttpResponse("Thank You",status=200)
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(MailchimpWebhookView,self).dispatch(request, *args, **kwargs)



