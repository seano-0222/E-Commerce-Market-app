"""
Views for the cart app (Malubay).

URL → View mapping:
    /cart/                  → view_cart       (show the customer's cart)
    /cart/add/<product_id>/ → add_to_cart     (add a product to the cart)
    /cart/remove/<item_id>/ → remove_from_cart (remove a cart item)
    /cart/clear/            → clear_cart      (empty the entire cart)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import Customer
from products.models import Product
from .models import Cart, CartItem
from .forms import CartForm  

def add_new_cart(request):
    """
    Add a new Cart record using a form (for lab requirement).
    """
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New cart record added successfully.')
            return redirect('/')  
    else:
        form = CartForm()

    return render(request, 'cart/addNewCart.html', {'form': form})


def _get_or_create_cart(customer):
    """Helper: get or create a Cart for the given Customer."""
    cart, _ = Cart.objects.get_or_create(customer=customer)
    return cart


# ---------------------------------------------------------------------------
# View: view_cart
# ---------------------------------------------------------------------------

def view_cart(request):
    """
    Display all items currently in the customer's cart.

    For demo purposes the first Customer in the DB is used as the
    'logged-in' customer. Once the login system is integrated this
    will use request.user → Customer lookup.
    """
    customer = Customer.objects.first()
    if not customer:
        messages.error(request, 'No customers exist yet. Please register a customer first.')
        return render(request, 'cart/cart.html', {'cart': None, 'items': []})

    cart  = _get_or_create_cart(customer)
    items = cart.items.select_related('product').all()

    return render(request, 'cart/cart.html', {
        'cart':  cart,
        'items': items,
    })


# ---------------------------------------------------------------------------
# View: add_to_cart
# ---------------------------------------------------------------------------

def add_to_cart(request, product_id):
    """
    Add a product to the current customer's cart.

    If the product is already in the cart, increment the quantity by 1.
    """
    customer = Customer.objects.first()
    if not customer:
        messages.error(request, 'No customers exist yet.')
        return redirect('view_cart')

    product = get_object_or_404(Product, pk=product_id)
    cart    = _get_or_create_cart(customer)

    # Check if already in cart — increase quantity instead of duplicating
    cart_item = cart.items.filter(product=product).first()
    if cart_item:
        cart_item.quantity += 1
        try:
            cart_item.save()
            messages.success(request, f'Added one more "{product.name}" to your cart.')
        except Exception as e:
            messages.error(request, str(e))
    else:
        try:
            CartItem.objects.create(cart=cart, product=product, quantity=1)
            messages.success(request, f'"{product.name}" added to your cart.')
        except Exception as e:
            messages.error(request, str(e))

    return redirect('view_cart')


# ---------------------------------------------------------------------------
# View: remove_from_cart
# ---------------------------------------------------------------------------

def remove_from_cart(request, item_id):
    """Remove a single CartItem from the cart."""
    cart_item = get_object_or_404(CartItem, pk=item_id)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'"{product_name}" removed from your cart.')
    return redirect('view_cart')


# ---------------------------------------------------------------------------
# View: clear_cart
# ---------------------------------------------------------------------------

def clear_cart(request):
    """Remove all items from the current customer's cart."""
    customer = Customer.objects.first()
    if customer:
        cart = _get_or_create_cart(customer)
        cart.items.all().delete()
        messages.success(request, 'Your cart has been cleared.')
    return redirect('view_cart')

