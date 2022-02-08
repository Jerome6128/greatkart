from django.contrib import admin

# Register your models here.
from orders.models import Payment, Order, OrderProduct

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)