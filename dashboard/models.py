from django.db import models

class Transaction(models.Model):
    date = models.DateField()
    order_id = models.CharField(max_length=64)
    product = models.CharField(max_length=128)
    category = models.CharField(max_length=64, blank=True)
    qty = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default='NGN')

    @property
    def amount(self):
        return float(self.qty) * float(self.unit_price)

    def __str__(self):
        return f"{self.order_id} | {self.product}"
