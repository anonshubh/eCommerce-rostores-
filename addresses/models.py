from django.db import models
from billing.models import BillingProfile
from django.utils.encoding import smart_str

ADDRESS_TYPE=[
    ('billing','Billing'),
    ('shipping','Shipping'),
]

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    address_type = models.CharField(max_length=128,choices=ADDRESS_TYPE)
    address_line_1 = models.CharField(max_length=128)
    address_line_2 = models.CharField(max_length=128,null=True,blank=True)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    country = models.CharField(max_length=50,default='India')
    postal_code = models.PositiveIntegerField()

    def __str__(self):
        return smart_str(self.billing_profile)

    def get_address(self):
        return f"{self.address_line_1}\n{self.city}\n{self.state}\n{self.postal_code}\n{self.country}"




