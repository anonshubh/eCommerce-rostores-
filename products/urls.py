from django.urls import path
from .views import product_detail,products_list,ProductDownloadView

app_name='products'

urlpatterns=[
    path('',products_list,name='list'),
    path('<slug>/',product_detail,name='detail'),
    path('<slug>/<pk>/',ProductDownloadView.as_view(),name='download'),
]