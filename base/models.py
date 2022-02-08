from django.db import models


# Create your models here.

class Asset(models.Model):
    ticker = models.CharField(max_length=8,unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ticker"]

    def __str__(self):
        return self.ticker

    # @classmethod
    # def create(cls, ticker):
    #     asset = cls(ticker=ticker)
    #     # do something with the book
    #     return asset
