from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Dummy data for prototyping
DUMMY_PRODUCTS = [
    {'uuid': '1', 'name': 'Coca-Cola 500ml', 'sku': 'SKU001', 'price': 100, 'thumbnail': 'https://placehold.co/40/5290F4/f0f0f0?font=museo&text=H'},
    {'uuid': '2', 'name': 'Fanta Orange 500ml', 'sku': 'SKU002', 'price': 100, 'thumbnail': 'https://placehold.co/40/5290F4/f0f0f0?font=museo&text=H'},
    {'uuid': '3', 'name': 'Sprite 500ml', 'sku': 'SKU003', 'price': 100, 'thumbnail': 'https://placehold.co/40/5290F4/f0f0f0?font=museo&text=H'},
    {'uuid': '4', 'name': 'Water 1L', 'sku': 'SKU004', 'price': 80, 'thumbnail': 'https://placehold.co/40/5290F4/f0f0f0?font=museo&text=H'},
]

DUMMY_CART = {
    'cart_uuid': 'cart-123',
    'items': [
        {'product': DUMMY_PRODUCTS[0], 'quantity': 2, 'subtotal': 200},
        {'product': DUMMY_PRODUCTS[3], 'quantity': 1, 'subtotal': 80},
    ],
    'total': 280,
    'discount': 0,
    'final_total': 280,
}

DUMMY_ORDER_SUMMARY = {
    'items': DUMMY_CART['items'],
    'total': DUMMY_CART['total'],
    'discount': DUMMY_CART['discount'],
    'final_total': DUMMY_CART['final_total'],
    'payment_methods': ['Cash', 'M-Pesa', 'Card'],
}

@login_required
def pos_main(request):
    """Main POS interface screen with dummy product list and cart."""
    context = {
        'products': DUMMY_PRODUCTS,
        'cart': DUMMY_CART,
        'concurrent_carts': [
            {'cart_uuid': 'cart-123', 'label': 'Cart 1', 'active': True},
            {'cart_uuid': 'cart-456', 'label': 'Cart 2', 'active': False},
        ],
    }
    return render(request, 'sales/pos/main.html', context)

@login_required
def cart_view(request):
    """View for the current cart with dummy items."""
    context = {
        'cart': DUMMY_CART,
        'concurrent_carts': [
            {'cart_uuid': 'cart-123', 'label': 'Cart 1', 'active': True},
            {'cart_uuid': 'cart-456', 'label': 'Cart 2', 'active': False},
        ],
    }
    return render(request, 'sales/pos/cart.html', context)

@login_required
def checkout_view(request):
    """Checkout/payment screen with dummy order summary."""
    context = {
        'order_summary': DUMMY_ORDER_SUMMARY,
        'concurrent_carts': [
            {'cart_uuid': 'cart-123', 'label': 'Cart 1', 'active': True},
            {'cart_uuid': 'cart-456', 'label': 'Cart 2', 'active': False},
        ],
    }
    return render(request, 'sales/pos/checkout.html', context)
