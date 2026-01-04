from django.db import models


class Payment(models.Model):
    student = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=100, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.amount}"
class PaymentReceipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    receipt_file = models.FileField(upload_to='payment_receipts/')
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt for {self.payment.student.user.username} - {self.payment.amount}"