from django.contrib import admin
from .models import Cart, Sale, SaleItem, Payment, Discount, Coupon, Promotion, Tip, Return, OrderNote, SaleItemNote

admin.site.register(Cart)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Payment)
admin.site.register(Discount)
admin.site.register(Coupon)
admin.site.register(Promotion)
admin.site.register(Tip)
admin.site.register(Return)
admin.site.register(OrderNote)
admin.site.register(SaleItemNote)
