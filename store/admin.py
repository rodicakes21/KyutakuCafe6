from django.contrib import admin
from .models import Order, Product, CheckoutItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "receipt_code", "payment_status", "created_at")
    search_fields = ("customer_name", "receipt_code")
    list_filter = ("payment_status", "created_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(CheckoutItem)
class CheckoutItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "total_price")

