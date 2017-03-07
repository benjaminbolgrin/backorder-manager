from backorder_manager.models import CustomerOrder, OrderItem


# Function to update the status on the CustomerOrder object
def co_update(co_id):

    exception = "CustomerOrder status could not be updated"

    try:
        customer_order = CustomerOrder.objects.get(pk=co_id)
        order_items = customer_order.orderitem_set.all()
        item_count = order_items.count()
        new_items = order_items.filter(status=OrderItem.new_status)
        received_items = order_items.filter(status=OrderItem.received_status)
        received_item_count = received_items.count()
        waiting_items = order_items.filter(status=OrderItem.ordered_status)
    except Exception:
        raise Exception(exception)

    # Check if all items are in stock
    if item_count == received_item_count:
        # Set the order status to complete
        customer_order.status = CustomerOrder.complete_status
        try:
            customer_order.save()
        except Exception:
            raise Exception(exception)

    # Check if there are new items related to the order
    if new_items:
        # Set the order status to pending
        customer_order.status = CustomerOrder.pending_status
        try:
            customer_order.save()
        except Exception:
            raise Exception(exception)

    # Check if we are waiting for related items
    if waiting_items and not new_items:
        # Set the order status to waiting
        customer_order.status = CustomerOrder.waiting_status
        try:
            customer_order.save()
        except Exception:
            raise Exception(exception)
