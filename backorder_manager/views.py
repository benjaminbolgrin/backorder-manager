from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView
from .models import CustomerOrder, OrderItem, Supplier
from django.core.urlresolvers import reverse_lazy
from .forms import ItemForm, ItemUpdateForm
from django.shortcuts import get_object_or_404, redirect, render
from datetime import date
from backorder_manager.utils import co_update
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


# This is the view for the dashboard. Users need view permissions for items and orders.
@permission_required('backorder_manager.view_item')
@permission_required('backorder_manager.view_order')
def dashboard(request):
    date_today = date.today()
    new_items = OrderItem.objects.filter(status=OrderItem.new_status)[:10]
    due_items = OrderItem.objects.filter(status=OrderItem.ordered_status, delivery_date__lt=date_today)[:10]
    complete_orders = CustomerOrder.objects.filter(status=CustomerOrder.complete_status).order_by('order_date')[:10]
    context = {
        'new_items': new_items,
        'due_items': due_items,
        'complete_orders': complete_orders
    }
    return render(request, 'backorder_manager/dashboard.html', context=context)


# This view returns the form to create a new order
class OrderCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'backorder_manager.add_customerorder'
    model = CustomerOrder
    template_name = 'backorder_manager/order-create.html'
    fields = ['order_number', 'order_date', 'first_name', 'last_name', 'phone', 'email', 'notice']

    # Show the orders details on success
    def get_success_url(self):
        return reverse_lazy('order_details', args=(self.object.id,))


# This view shows an orders details
class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = 'backorder_manager.view_order'
    model = CustomerOrder
    template_name = 'backorder_manager/order-details.html'


# This view returns the form to update an order
class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'backorder_manager.change_customerorder'
    model = CustomerOrder
    template_name = 'backorder_manager/order-update.html'
    fields = ['order_number', 'order_date', 'first_name', 'last_name', 'phone', 'email', 'notice']


# This view shows all items with a 'pending' status
class ItemsPendingView(PermissionRequiredMixin, ListView):
    permission_required = 'backorder_manager.view_item'
    model = OrderItem
    paginate_by = 15
    template_name = 'backorder_manager/items-pending.html'

    def get_queryset(self):
        queryset = OrderItem.objects.all().filter(status=OrderItem.new_status).order_by('-supplier')
        return queryset


# This view shows all items with a 'waiting' status
class ItemsWaitingView(PermissionRequiredMixin, ListView):
    permission_required = 'backorder_manager.view_item'
    model = OrderItem
    template_name = 'backorder_manager/items-waiting.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = OrderItem.objects.filter(status=OrderItem.ordered_status).order_by('delivery_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ItemsWaitingView, self).get_context_data(**kwargs)
        context['date_today'] = date.today
        return context


# This view updates the status of an item to 'ordered' and sets the order_date to today
@permission_required('backorder_manager.change_orderitem')
def item_ordered(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)
    if item:
        item.status = OrderItem.ordered_status
        item.order_date = date.today()
        item.save()
        # Update CustomerOrder status
        co_update.co_update(item.customer_order.pk)
    return redirect(reverse_lazy('items_pending'))


# This view updates the status of an item to 'received' and sets the delivery_date to today
@permission_required('backorder_manager.change_orderitem')
def item_receive(request, pk):
    item = get_object_or_404(OrderItem, pk=pk)
    if item:
        item.status = OrderItem.received_status
        item.delivery_date = date.today()
        item.save()
        # Update CustomerOrder status
        co_update.co_update(item.customer_order.pk)
    return redirect(reverse_lazy('items_waiting'))


# This view displays all orders with the 'complete' status
class OrdersCompleteView(PermissionRequiredMixin, ListView):
    permission_required = 'backorder_manager.view_order'
    model = CustomerOrder
    fields = ['name', 'supplier']
    template_name = 'backorder_manager/orders-complete.html'


# This view is for deletion of an order
class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'backorder_manager.delete_customerorder'
    model = CustomerOrder
    template_name = 'backorder_manager/order-delete.html'
    success_url = reverse_lazy('order_delete_success')


# This view is returned after successful deletion of an order
class OrderDeleteSuccessView(TemplateView):
    template_name = 'backorder_manager/order-delete-success.html'


# Add items to orders through this view
class ItemCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'backorder_manager.add_orderitem'
    model = OrderItem
    form_class = ItemForm
    template_name = 'backorder_manager/item-create.html'

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        order = CustomerOrder.objects.get(id=self.kwargs['order_id'])
        context['order_number'] = order.order_number
        context['customer_first_name'] = order.first_name
        context['customer_last_name'] = order.last_name
        context['customer_order_id'] = order.pk
        return context

    # Save item to database and update CustomerOrder status
    def form_valid(self, form):
        form.save()
        co_update.co_update(self.kwargs['order_id'])
        return super(ItemCreateView, self).form_valid(form)

    # Return to the order details on success
    def get_success_url(self):
        return reverse_lazy('order_details', args=(self.kwargs['order_id'],))


# This view is used to edit item details
class ItemUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'backorder_manager.change_orderitem'
    model = OrderItem
    form_class = ItemUpdateForm
    template_name = 'backorder_manager/item-update.html'

    def get_context_data(self, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(**kwargs)
        customer_order = self.object.customer_order
        context['customer_order'] = customer_order
        return context

    # Save item to database and update CustomerOrder status
    def form_valid(self, form):
        form.save()
        item = OrderItem.objects.get(pk=self.kwargs['pk'])
        customer_order = item.customer_order.pk
        co_update.co_update(customer_order)
        return super(ItemUpdateView, self).form_valid(form)

    # Return to order details on success
    def get_success_url(self):
        order = self.object.customer_order
        order_number = order.pk
        return reverse_lazy('order_details', args=(order_number,))


# This view is used to delete an item
@permission_required('backorder_manager.delete_orderitem')
def item_delete(request, pk):

    # Show delete dialog
    if request.method == 'GET':
        item = get_object_or_404(OrderItem, pk=pk)
        customer_order = item.customer_order
        context = {
            'customer_order': customer_order,
            'object': item
        }
        return render(request, template_name='backorder_manager/item-delete.html', context=context)

    # Start deletion
    if request.method == 'POST':
        item = get_object_or_404(OrderItem, pk=pk)
        customer_order = item.customer_order
        customer_order_id = customer_order.pk
        # Delete the item
        item.delete()
        # Update order status
        co_update.co_update(customer_order_id)
        # Return to order details on success
        return redirect(reverse_lazy('order_details', kwargs={'pk': customer_order_id}))


# This view is used to show the details of an supplier
class SupplierDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'backorder_manager.view_supplier'
    model = Supplier
    template_name = 'backorder_manager/supplier-details.html'
    fields = ['name', 'phone', 'email', 'customer-number']


# This is the view for menu entry 'Orders'
@permission_required('backorder_manager.view_order')
def orders(request):
    return render(request, template_name='backorder_manager/orders.html')


# The list of all orders ordered by it's status
class OrderListView(PermissionRequiredMixin, ListView):
    permission_required = 'backorder_manager.view_order'
    model = CustomerOrder
    template_name = 'backorder_manager/order-list.html'
    paginate_by = 15
    fields = ['status', 'first_name', 'last_name', 'order_date']

    def get_queryset(self):
        queryset = CustomerOrder.objects.all().order_by('status')
        return queryset


# When you click on 'Complete' in the top navigation, this view is returned
class OrderCompleteView(PermissionRequiredMixin, ListView):
    permission_required = 'backorder_manager.view_order'
    model = CustomerOrder
    template_name = 'backorder_manager/orders-complete.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = CustomerOrder.objects.filter(status=CustomerOrder.complete_status).order_by('order_date')
        return queryset


# When you click on the 'archive' button, this view is used
@permission_required('backorder_manager.change_customerorder')
def order_archive(request, pk):
    customer_order = get_object_or_404(
        CustomerOrder,
        pk=pk,
        status=CustomerOrder.complete_status
        )
    order_items = OrderItem.objects.filter(customer_order=customer_order)
    # Set related item's status to closed
    for item in order_items:
        item.status = OrderItem.closed_status
        item.save()
    # Set order status to archive
    customer_order.status = CustomerOrder.archive_status
    customer_order.save()
    # Return to the list of complete orders
    return render(request, template_name='backorder_manager/orders-complete.html')
