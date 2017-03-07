from django.contrib import admin
from .models import CustomerOrder, OrderItem, Supplier

admin.site.register(CustomerOrder)
admin.site.register(OrderItem)
admin.site.register(Supplier)