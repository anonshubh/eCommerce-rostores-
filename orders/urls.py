from django.urls import path
from .views import OrderDetailView,OrderListView,LibraryView

app_name = 'orders'

urlpatterns=[
    path('',OrderListView.as_view(),name='list'),
    path('detail/<order_id>/',OrderDetailView.as_view(),name='detail'),
    path('library/',LibraryView.as_view(),name='library'),
]
