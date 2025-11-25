from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation
import uuid

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Auto receipt number
    receipt_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # Customer Information (Only name now)
    customer_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    # ----------------------------
    # PAYMENT STATUS
    # ----------------------------
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("unpaid", "Unpaid"),
            ("pending", "Pending"),
            ("paid", "Paid")
        ],
        default="unpaid"
    )

    # Cashier fields
    cash_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    change_given = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Optional payment screenshot
    payment_screenshot = models.ImageField(upload_to="payments/", blank=True, null=True)

    # ----------------------------
    # TOTAL PRICE CALCULATION
    # ----------------------------
    def total_price(self):
        total = Decimal("0")
        for item in self.items.all():
            try:
                total += Decimal(item.total_price)
            except (InvalidOperation, ValueError, TypeError):
                total += Decimal(item.quantity) * Decimal(item.product.price)
        return total

    # ----------------------------
    # AUTO RECEIPT CODE
    # ----------------------------
    def save(self, *args, **kwargs):
        if not self.receipt_code:
            self.receipt_code = "RCP-" + uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"



class CheckoutItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} = ₱{self.total_price}"

