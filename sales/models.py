# Django imports
from django.db import models
from django.conf import settings

# Python imports
import uuid


# Create your models here.
class Cart(models.Model):
    """
    A cart for a user to add items to before checkout.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Sale(models.Model):
    """
    A sale is a completed transaction.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    cart = models.ForeignKey('Cart', on_delete=models.SET_NULL, null=True, blank=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class SaleItem(models.Model):
    """
    An item in a sale.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Payment(models.Model):
    """
    A payment for a sale.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=50)  # e.g., cash, mpesa, card
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

class Discount(models.Model):
    """
    A discount for a sale.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, null=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Coupon(models.Model):
    """
    A coupon for a sale.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    code = models.CharField(max_length=50, unique=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE)
    
    is_active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class Promotion(models.Model):
    """
    A promotion for a sale.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tip(models.Model):
    """
    A tip for a sale. This is a tip for the seller.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='tips')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)

class Return(models.Model):
    """
    A return for a sale. This is a return for the customer.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='returns')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

class OrderNote(models.Model):
    """
    A note for a sale. This is a note for the seller.
    """
    
    sale = models.OneToOneField('Sale', on_delete=models.CASCADE, related_name='note')
    note = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

class SaleItemNote(models.Model):
    """
    A note for an item in a sale. This is a note for the seller.
    """
    
    sale_item = models.OneToOneField('SaleItem', on_delete=models.CASCADE, related_name='note')
    note = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
