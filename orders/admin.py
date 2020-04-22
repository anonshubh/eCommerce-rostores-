from django.contrib import admin

from .models import Order

class OrderAdmin(admin.ModelAdmin):
    readonly_fields=['order_id']

admin.site.register(Order,OrderAdmin)
