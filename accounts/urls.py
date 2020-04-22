from django.urls import path
from .views import login_page,register_page,guest_register_page
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns=[
    path('login/',login_page,name='login_url'),
    path('register/guest/',guest_register_page,name='guest_register'),
    path('register/',register_page,name='register_url'),
    path('logout/',LogoutView.as_view(),name='logout_url'),
]