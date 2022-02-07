from django.db import models


# Create your models here.

class Asset(models.Model):
    ticker = models.CharField(null=False, max_length=6, unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ticker = self.ticker
