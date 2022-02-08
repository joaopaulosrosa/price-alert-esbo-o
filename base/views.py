from django.shortcuts import render
import requests
from .models import Asset

# Create your views here.

def home(request):
    assets = Asset.objects.all()
    ad = assets.filter(ticker="AALR3")
    context = {
        'assets': assets,
        'ad': ad
        }
    return render(request, 'base/home.html', context)
