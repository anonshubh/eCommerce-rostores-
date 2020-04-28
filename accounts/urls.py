from django.urls import path
from .views import LoginView,RegisterView,GuestRegisterView,AccountHomeView,AccountEmailActivateView,UserDetailUpdateView
from django.contrib.auth.views import LogoutView
from products.views import UserProductHistoryView

app_name = 'accounts'

urlpatterns=[
    path('login/',LoginView.as_view(),name='login_url'),
    path('register/guest/',GuestRegisterView.as_view(),name='guest_register'),
    path('register/',RegisterView.as_view(),name='register_url'),
    path('logout/',LogoutView.as_view(),name='logout_url'),
    path('',AccountHomeView.as_view(),name='home'),
    path('email/confirm/<key>/',AccountEmailActivateView.as_view(),name='email-activate'),
    path('email/resend/activation/',AccountEmailActivateView.as_view(),name='email-reactivate'),
    path('update/',UserDetailUpdateView.as_view(),name='update_details'),
    path('history/product/',UserProductHistoryView.as_view(),name = 'product_history')
]