# Django imports
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from django.db import transaction

# Python imports
import json
import logging
from decimal import Decimal

# Project imports
from accounts.models import UserActionLog
from inventory.models import Product
from .models import Cart, Sale, SaleItem, Payment, Discount, Coupon, Tip, Return

# Initialize logger
logger = logging.getLogger(__name__)

@login_required
@require_GET
def get_active_cart(request):
    """Get or create an active cart for the current user."""
    try:
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
        
        # Get cart items (implement this based on your needs)
        items = []  # You'll need to implement this
        
        return JsonResponse({
            'cart_uuid': str(cart.uuid),
            'items': items,
            'created_at': cart.created_at.isoformat(),
            'updated_at': cart.updated_at.isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting active cart: {str(e)}")
        return JsonResponse({'error': 'Failed to get active cart.'}, status=500)

@login_required
@require_POST
@csrf_exempt
def add_to_cart(request):
    """Add an item to the cart."""
    try:
        data = json.loads(request.body.decode())
        product_uuid = data.get('product_uuid')
        quantity = int(data.get('quantity', 1))
        
        if not product_uuid:
            return JsonResponse({'error': 'Product UUID is required.'}, status=400)
            
        # Get or create active cart
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
            
        # Get product
        try:
            product = Product.objects.get(uuid=product_uuid)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
            
        # Add to cart (implement your cart item logic here)
        # This is a placeholder - implement according to your needs
        
        return JsonResponse({
            'message': 'Item added to cart.',
            'cart_uuid': str(cart.uuid)
        })
    except Exception as e:
        logger.error(f"Error adding to cart: {str(e)}")
        return JsonResponse({'error': 'Failed to add item to cart.'}, status=500)

@login_required
@require_POST
@csrf_exempt
def remove_from_cart(request):
    """Remove an item from the cart."""
    try:
        data = json.loads(request.body.decode())
        product_uuid = data.get('product_uuid')
        
        if not product_uuid:
            return JsonResponse({'error': 'Product UUID is required.'}, status=400)
            
        # Get active cart
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            return JsonResponse({'error': 'No active cart found.'}, status=404)
            
        # Remove from cart (implement your cart item removal logic here)
        # This is a placeholder - implement according to your needs
        
        return JsonResponse({
            'message': 'Item removed from cart.',
            'cart_uuid': str(cart.uuid)
        })
    except Exception as e:
        logger.error(f"Error removing from cart: {str(e)}")
        return JsonResponse({'error': 'Failed to remove item from cart.'}, status=500)

@login_required
@require_POST
@csrf_exempt
def apply_discount(request):
    """Apply a discount to the cart."""
    try:
        data = json.loads(request.body.decode())
        discount_code = data.get('code')
        
        if not discount_code:
            return JsonResponse({'error': 'Discount code is required.'}, status=400)
            
        # Get active cart
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            return JsonResponse({'error': 'No active cart found.'}, status=404)
            
        # Validate and apply discount
        try:
            discount = Discount.objects.get(code=discount_code, is_active=True)
            # Apply discount logic here
            
            return JsonResponse({
                'message': 'Discount applied successfully.',
                'discount_amount': str(discount.amount) if discount.amount else str(discount.percent)
            })
        except Discount.DoesNotExist:
            return JsonResponse({'error': 'Invalid discount code.'}, status=400)
            
    except Exception as e:
        logger.error(f"Error applying discount: {str(e)}")
        return JsonResponse({'error': 'Failed to apply discount.'}, status=500)

@login_required
@require_POST
@csrf_exempt
@transaction.atomic
def process_payment(request):
    """Process payment and create sale."""
    try:
        data = json.loads(request.body.decode())
        cart_uuid = data.get('cart_uuid')
        payment_method = data.get('payment_method')
        amount = Decimal(data.get('amount', '0'))
        
        if not all([cart_uuid, payment_method, amount]):
            return JsonResponse({'error': 'Cart UUID, payment method, and amount are required.'}, status=400)
            
        # Get cart
        try:
            cart = Cart.objects.get(uuid=cart_uuid, is_active=True)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found.'}, status=404)
            
        # Create sale and payment
        with transaction.atomic():
            # Create sale
            sale = Sale.objects.create(
                cart=cart,
                user=request.user,
                total=amount,
                completed_at=timezone.now()
            )
            
            # Create payment
            payment = Payment.objects.create(
                sale=sale,
                method=payment_method,
                amount=amount
            )
            
            # Deactivate cart
            cart.is_active = False
            cart.save()
            
            # Log the transaction
            UserActionLog.objects.create(
                user=request.user,
                action='sale_completed',
                details=f'Sale {sale.uuid} completed with {payment_method}',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
        return JsonResponse({
            'message': 'Payment processed successfully.',
            'sale_uuid': str(sale.uuid),
            'payment_uuid': str(payment.uuid)
        })
            
    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        return JsonResponse({'error': 'Failed to process payment.'}, status=500)

@login_required
@require_POST
@csrf_exempt
def process_return(request):
    """Process a return/refund."""
    try:
        data = json.loads(request.body.decode())
        sale_uuid = data.get('sale_uuid')
        reason = data.get('reason')
        
        if not sale_uuid:
            return JsonResponse({'error': 'Sale UUID is required.'}, status=400)
            
        # Get sale
        try:
            sale = Sale.objects.get(uuid=sale_uuid)
        except Sale.DoesNotExist:
            return JsonResponse({'error': 'Sale not found.'}, status=404)
            
        # Create return
        return_obj = Return.objects.create(
            sale=sale,
            user=request.user,
            reason=reason
        )
        
        # Log the return
        UserActionLog.objects.create(
            user=request.user,
            action='return_processed',
            details=f'Return {return_obj.uuid} processed for sale {sale.uuid}',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Return processed successfully.',
            'return_uuid': str(return_obj.uuid)
        })
            
    except Exception as e:
        logger.error(f"Error processing return: {str(e)}")
        return JsonResponse({'error': 'Failed to process return.'}, status=500) 