from django.urls import path
from .views import checkout_address_create_view,checkout_address_reuse_view


urlpatterns=[
    path('address/create/',checkout_address_create_view,name='address_create'),
    path('address/reuse/',checkout_address_reuse_view,name='address_reuse'),
]