from django.urls import path
from .views import checkout_address_create_view,checkout_address_reuse_view,AddressCreateView,AddressListView,AddressUpdateView


urlpatterns=[
    path('address/create/',checkout_address_create_view,name='address_create'),
    path('address/reuse/',checkout_address_reuse_view,name='address_reuse'),
    path('addresses/',AddressListView.as_view(),name = 'addresses'),
    path('address/create/',AddressCreateView.as_view(),name = 'address-create'),
    path('address/update/<pk>',AddressUpdateView.as_view(),name='address-update'),

]
