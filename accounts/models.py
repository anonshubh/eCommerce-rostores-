import random
from datetime import timezone,timedelta
from django.utils import timezone
from django.db import models
from django.utils.encoding import smart_str
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.mail import send_mail
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from ecommerce_src.utils import random_string_generator,unique_key_generator


class UserManager(BaseUserManager):
    def create_user(self,email,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError("Email ID is Mandatory")
        if not password:
            raise ValueError("Password is Mandatory")
        user_obj = self.model(
            email = self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self,email,password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
        )
        return user
    
    def create_superuser(self,email,password=None):
        user = self.create_user(
            email,
            password=password,
            is_admin=True,
            is_staff=True,
        )
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True,max_length=256)
    full_name = models.CharField(max_length = 256,default='')
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return smart_str(self.email)

    def get_full_name(self):
        if self.full_name:
            return smart_str(self.full_name)
        else:
            return smart_str(self.email)

    def get_short_name(self):
        return smart_str(self.email)
    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_superuser(self):
        if self.admin and self.staff:
            return True
        return False
    
class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return smart_str(self.email)

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=7)
        end_range = now
        return self.filter(activated=False,forced_expired=False).filter(timestamp__gt=start_range,timestamp__lte=end_range)

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model,using=self._db)
    
    def confirmable(self):
        return self.get_queryset().confirmable()

class EmailActivation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=128,blank=True,null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return smart_str(self.email)
    
    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False
    
    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False
    
    def send_activation_email(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings,'BASE_URL')
                key_path = reverse('accounts:email-activate',kwargs={'key':self.key})
                path = f"{base_url}{key_path}"
                context={
                    'path':path,
                    'email':self.email,
                }
                txt_ = get_template('registration/emails/verify.txt').render(context)
                html_ = get_template('registration/emails/verify.html').render(context)
                subject = "Email Verification"
                from_email = settings.DEFAULT_FROM_MAIL
                recipient_list = [self.email]
                send_email = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message = html_,
                    fail_silently = False,
                )
                print("Email send")
                return send_email
        return False
    
def pre_save_email_activation(sender,instance,*args,**kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation,sender=EmailActivation)

def post_save_user_create_receiver(sender,instance,created,*args,**kwargs):
    if created:
        obj= EmailActivation.objects.create(user=instance,email=instance.email)
        obj.send_activation_email()

post_save.connect(post_save_user_create_receiver,sender=User)




    

 