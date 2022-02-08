from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Asset(models.Model):
    ticker = models.CharField(max_length=8,unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ticker"]

    def __str__(self):
        return self.ticker


class AlarmAsset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    buying_price = models.DecimalField(max_digits=30, decimal_places=2)
    selling_price = models.DecimalField(max_digits=30, decimal_places=2)
    saving_interval = models.IntegerField

    def __str__(self):
        return self.asset
