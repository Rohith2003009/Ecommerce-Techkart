from django.shortcuts import render, redirect
from .models import Product, CartItem
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import cartData
from .models import Product, Order, OrderItem, Customer # Adjust if your models are elsewhere
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404


def home(request):
    products = Product.objects.all()[:15]
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')  # make sure you have a 'login' path name in your urls
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    return render(request, 'store/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

def cart_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total = 0

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


@login_required
def place_order(request):
    data = cartData(request)
    items = data['items']

    if items:
        # Create an Order instance
        order = Order.objects.create(user=request.user, complete=True)

        for item in items:
            product = item['product']
            quantity = item['quantity']

            OrderItem.objects.create(
                order=order,
                product=Product.objects.get(id=product['id']),
                quantity=quantity
            )

        # Clear cart after order is placed
        request.session['cart'] = {}  # if you're using session cart
        return redirect('home')  # or a success page
    return redirect('cart')


def place_order(request):
    if request.method == 'POST':
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        total = sum(item.product.price * item.quantity for item in cart_items)

        if total < 100:
            messages.error(request, "Minimum order value is ₹100.")
            return redirect('cart')
        elif total > 10000:
            messages.error(request, "Maximum order value is ₹10,000.")
            return redirect('cart')

        # Proceed with order placement logic
        # Create Order instance, clear cart, etc.

        return redirect('order_success')
 # Make sure CartItem is imported

def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        action = request.POST.get('action')

        if action == 'increase' and item.quantity < 10:
            item.quantity += 1
        elif action == 'decrease' and item.quantity > 1:
            item.quantity -= 1

        item.save()

    return redirect('cart')

def delete_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')
def place_order(request):
    if request.method == 'POST':
        # Example logic – adjust based on your actual model handling
        customer = request.user.customer  # or however you associate the user
        order = Order.objects.get(customer=customer, complete=False)
        order.complete = True
        order.save()

        return redirect('order_success')  # <<< redirect here after placing order

    return redirect('cart')


def order_success(request):
    return render(request, 'store/order_success.html')  # Make sure this template exists