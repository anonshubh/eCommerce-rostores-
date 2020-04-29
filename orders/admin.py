from django.contrib import admin

from .models import Order,ProductPurchase

class OrderAdmin(admin.ModelAdmin):
    readonly_fields=['order_id']

admin.site.register(Order,OrderAdmin)
admin.site.register(ProductPurchase)
