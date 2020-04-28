from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .signals import object_viewed_signal
from .utils import get_client_ip
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save,post_save
from accounts.signals import user_logged_in
from django.utils.encoding import smart_str

User = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings,'FORCE_SESSION_TO_ONE',False)

FORCE_INACTIVE_USER_ENDSESSION = getattr(settings,'FORCE_INACTIVE_USER_ENDSESSION',False)

class ObjectViewed(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    ip_address = models.CharField(max_length = 128,null=True,blank=True)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s was viewed on %s" %(self.content_object,self.timestamp)
    
    class Meta():
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

def object_viewed_receiver(sender,instance,request,*args,**kwargs):
    content_type = ContentType.objects.get_for_model(sender)
    user = None
    if request.user.is_authenticated:
        user = request.user
    new_view_obj = ObjectViewed.objects.create(
        user = user,
        ip_address = get_client_ip(request),
        object_id = instance.id,
        content_type = content_type,
    )

object_viewed_signal.connect(object_viewed_receiver)

class UserSession(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    ip_address = models.CharField(max_length = 128,null=True,blank=True)
    session_key = models.CharField(max_length=128,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def __str__(self):
        return smart_str(self.user)

    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended

def post_save_session_receiver(sender,instance,created,*args,**kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user,ended=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

def post_save_user_changed_receiver(sender,instance,created,*args,**kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance.user,ended=False,active=False)
            for i in qs:
                i.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver,sender=UserSession)

if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver,sender=User)

def user_logged_in_receiver(sender,instance,request,*args,**kwagrs):
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    user = instance
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key = session_key
    )

user_logged_in.connect(user_logged_in_receiver)

