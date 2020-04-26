from django.db import models
from django.utils.encoding import smart_str
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,full_name,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError("Email ID is Mandatory")
        if not password:
            raise ValueError("Password is Mandatory")
        if not full_name:
            raise ValueError("Name is Required")
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self,full_name,email,password=None):
        user = self.create_user(
            email,
            full_name = full_name,
            password=password,
            is_staff=True,
        )
        return user
    
    def create_superuser(self,full_name,email,password=None):
        user = self.create_user(
            email,
            full_name = full_name,
            password=password,
            is_admin=True,
            is_staff=True,
        )
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True,max_length=256)
    full_name = models.CharField(max_length = 256,default='')
    active = models.BooleanField(default=True)
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
        return smart_str(self.full_name)

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
    
    # @property
    # def is_active(self):
    #     return self.active


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return smart_str(self.email)
    

 