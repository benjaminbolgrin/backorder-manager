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
from django.contrib.auth.views import login, logout
import views
import settings



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', login, {'template_name': 'backorder_manager/login.html'},
        name='login'),
    url(r'^logout/$', logout, {'template_name': 'backorder_manager/login.html',
                               'next_page': '/login/'},
        name='logout'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^order-list/$', views.OrderListView.as_view(), name='order_list'),
    url(r'^order-create/$', views.OrderCreateView.as_view(), name='order_create'),
    url(r'^order-edit/(?P<pk>[0-9]+)/$', views.OrderUpdateView.as_view(), name='order_update'),
    url(r'^order-details/(?P<pk>[0-9]+)/$', views.OrderDetailsView.as_view(), name='order_details'),
    url(r'^order-delete/(?P<pk>[0-9]+)/$', views.OrderDeleteView.as_view(), name='order_delete'),
    url(r'^order-delete-success/$', views.OrderDeleteSuccessView.as_view(), name='order_delete_success'),
    url(r'^orders-complete/$', views.OrderCompleteView.as_view(), name='orders_complete'),
    url(r'^orders-archive/(?P<pk>[0-9]+)/$', views.order_archive, name='order_archive'),
    url(r'^items-pending/$', views.ItemsPendingView.as_view(), name='items_pending'),
    url(r'^items-waiting/$', views.ItemsWaitingView.as_view(), name='items_waiting'),
    url(r'^item-create/(?P<order_id>[0-9]+)$', views.ItemCreateView.as_view(), name='item_create'),
    url(r'^item-edit/(?P<pk>[0-9]+)/$', views.ItemUpdateView.as_view(), name='item_update'),
    url(r'^item-delete/(?P<pk>[0-9]+)/$', views.item_delete, name='item_delete'),
    url(r'^item-ordered/(?P<pk>[0-9]+)/$', views.item_ordered, name='item_ordered'),
    url(r'^item-receive/(?P<pk>[0-9]+)/$', views.item_receive, name='item_receive'),
    url(r'^supplier-detail/(?P<pk>[0-9]+)/$', views.SupplierDetailView.as_view(), name='supplier_detail'),
    url(r'^administration/', include('administration.urls')),
]
