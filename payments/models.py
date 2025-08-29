from django.db import models
from django.conf import settings
from materials.models import Course  # курс, который покупаем

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments")
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)  # ID платежа в Stripe
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="pending")  # pending, succeeded, failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.course} ({self.amount}₽)"
