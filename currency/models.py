from django.db import models

class CurrencyRate(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    rate = models.FloatField()

    class Meta:
        ordering = ['-timestamp']
