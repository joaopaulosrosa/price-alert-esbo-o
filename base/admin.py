from django.contrib import admin

# Register your models here.

from .models import AlarmAsset, Asset, AssetPriceHistory

admin.site.register(Asset)
admin.site.register(AlarmAsset)
admin.site.register(AssetPriceHistory)
