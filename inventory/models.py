# Django imports
from django.db import models

# Python imports
import uuid

# Create your models here.

class Product(models.Model):
    """
    A product is a physical item that can be sold.
    """
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sku = models.CharField(max_length=512, unique=True)
    
    name = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
