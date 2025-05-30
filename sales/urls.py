from django.urls import path
from . import api, views

# views
urlpatterns = [
    path('pos/', views.pos_main, name='pos_main'),
    path('pos/cart/', views.cart_view, name='pos_cart'),
    path('pos/checkout/', views.checkout_view, name='pos_checkout'),
    # Add view URLs here when we create the frontend
]

# api
urlpatterns += [
    path('api/cart/active/', api.get_active_cart, name='api_get_active_cart'),
    path('api/cart/add/', api.add_to_cart, name='api_add_to_cart'),
    path('api/cart/remove/', api.remove_from_cart, name='api_remove_from_cart'),
    path('api/discount/apply/', api.apply_discount, name='api_apply_discount'),
    path('api/payment/process/', api.process_payment, name='api_process_payment'),
    path('api/return/process/', api.process_return, name='api_process_return'),
] 