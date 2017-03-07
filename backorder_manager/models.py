from __future__ import unicode_literals
from django.db import models
from datetime import date


class Supplier(models.Model):
    name = models.CharField(max_length=80, verbose_name='Supplier name')
    phone = models.CharField(max_length=80, null=True, blank=True, verbose_name='Phone number')
    email = models.EmailField(blank=True, verbose_name='Email')
    customer_number = models.CharField(max_length=80, blank=True, verbose_name='Customer number')

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("view.suppliers", "Can see supplier information"),
        )


class CustomerOrder(models.Model):

    pending_status = 1
    waiting_status = 2
    complete_status = 3
    archive_status = 4

    status_choices = (
        (pending_status, 'New'),
        (waiting_status, 'Waiting'),
        (complete_status, 'Complete'),
        (archive_status, 'Archived'))

    order_number = models.CharField(max_length=80, null=True)
    order_date = models.DateField(default=date.today, verbose_name='Order date (YYYY-MM-DD)')
    complete_date = models.DateField(blank=True, verbose_name='Order completion date', null=True)
    notice = models.CharField(max_length=420, blank=True, verbose_name='Order notice')
    status = models.IntegerField(choices=status_choices, default=pending_status, verbose_name='Order status')
    first_name = models.CharField(max_length=80, verbose_name='Customer first name', null=True)
    last_name = models.CharField(max_length=80, verbose_name='Customer last name' , null=True)
    phone = models.CharField(max_length=80, blank=True, verbose_name='Customer phone number', null=True)
    email = models.EmailField(blank=True, verbose_name='Customer email', null=True)

    def __str__(self):
        return '#' + str(self.order_number) + ' ' + str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        permissions = (
            ("view_order", "Can see order information"),
        )


class OrderItem(models.Model):

    new_status = 1
    ordered_status = 2
    received_status = 3
    closed_status = 4

    status_choices = (
        (new_status, 'New'),
        (ordered_status, 'Ordered'),
        (received_status, 'Received'),
        (closed_status, 'Closed'))

    customer_order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier)
    number = models.CharField(max_length=80, blank=True, verbose_name='Item number', null=True)
    name = models.CharField(max_length=120, verbose_name='Item name')
    quantity = models.IntegerField(default=1, verbose_name='Quantity ordered')
    status = models.IntegerField(choices=status_choices, default=new_status,verbose_name='Item status')
    delivery_date = models.DateField(blank=True, verbose_name='Delivery date (YYYY-MM-DD)', null=True)
    order_date = models.DateField(blank=True, verbose_name='Order date (YYYY-MM-DD)', null=True)

    def __str__(self):
        return self.supplier.name + ' ' + self.name

    class Meta:
        permissions = (
            ("view_item", "Can see item information"),
        )

