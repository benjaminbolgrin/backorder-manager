from django.contrib.auth.models import User
from django import forms
from .models import OrderItem
from django.forms.widgets import TextInput
import settings


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class ItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ['supplier', 'number', 'name', 'quantity', 'delivery_date', 'status', 'order_date', 'customer_order']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }


class ItemUpdateForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ['supplier', 'number', 'name', 'quantity', 'delivery_date', 'status', 'order_date']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }
