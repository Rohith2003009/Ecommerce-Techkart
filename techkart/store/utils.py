from .models import Product, Order, OrderItem
from django.contrib.auth.models import User

def cartData(request):
    """
    Returns cart data for both authenticated and guest users.
    Handles cart logic using session.
    """
    if request.user.is_authenticated:
        # Logged-in user
        try:
            order = Order.objects.get(user=request.user, complete=False)
        except Order.DoesNotExist:
            order = Order.objects.create(user=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = sum([item.quantity for item in items])
    else:
        # Guest user — use session cart
        session_cart = request.session.get('cart', {})
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0

        for product_id, quantity in session_cart.items():
            try:
                product = Product.objects.get(id=product_id)
                total = product.price * quantity

                order['get_cart_total'] += total
                order['get_cart_items'] += quantity

                item = {
                    'product': product,
                    'quantity': quantity
                }
                items.append(item)
                cartItems += quantity
            except Product.DoesNotExist:
                continue

    return {
        'cartItems': cartItems,
        'order': order,
        'items': items
    }