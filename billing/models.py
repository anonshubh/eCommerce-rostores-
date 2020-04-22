from django.db import models
from django.conf import settings
from django.utils.encoding import smart_str
from django.db.models.signals import post_save
from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def get_or_new(self,request):
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if request.user.is_authenticated:
            if request.user.email:
                obj,created = self.model.objects.get_or_create(user=request.user,email=request.user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj,created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return obj,created

class BillingProfile(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BillingProfileManager()

    def __str__(self):
        return smart_str(self.email)

# def billing_profile_created_receiver(sender,instance,created,*args,**kwargs):
#     if created:
#         print("API Request,Send to paytm")
#         instance.customer_id = newID
#         instance.save()

def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(user_created_receiver,sender=User)

