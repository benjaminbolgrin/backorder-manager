"""backorder_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import views

app_name = 'administration'

urlpatterns = [
    url(r'^$', views.administration, name='administration'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/create/$', views.UserCreateView.as_view(), name='user_create'),
    url(r'^users/list/$', views.UserListView.as_view(), name='user_list'),
    url(r'^users/delete/(?P<pk>[0-9]+)/$', views.UserDeleteView.as_view(), name='user_delete'),
    url(r'^users/edit/(?P<pk>[0-9]+)/$', views.UserUpdateView.as_view(), name='user_update'),
    url(r'^users/edit/password/(?P<pk>[0-9]+)/$', views.UserPasswordView.as_view(), name='user_password'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^groups/create/$', views.GroupCreateView.as_view(), name='group_create'),
    url(r'^groups/list/$', views.GroupListView.as_view(), name='group_list'),
    url(r'^groups/delete/(?P<pk>[0-9]+)/$', views.GroupDeleteView.as_view(), name='group_delete'),
    url(r'^groups/edit/(?P<pk>[0-9]+)/$', views.GroupUpdateView.as_view(), name='group_update'),
    url(r'^suppliers/$', views.suppliers, name='suppliers'),
    url(r'^suppliers/create/$', views.SupplierCreateView.as_view(), name='supplier_create'),
    url(r'^suppliers/list/$', views.SupplierListView.as_view(), name='supplier_list'),
    url(r'^suppliers/delete/(?P<pk>[0-9]+)/$', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    url(r'^suppliers/edit/(?P<pk>[0-9]+)/$', views.SupplierUpdateView.as_view(), name='supplier_update'),

]
