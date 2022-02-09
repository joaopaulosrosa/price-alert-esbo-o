from django.shortcuts import render
import requests
from .models import Asset
from .forms import AlarmAssetForm

# Create your views here.

def home(request):
    assets = Asset.objects.all()
    ad = assets.filter(ticker="AALR3")
    context = {
        'assets': assets,
        'ad': ad
        }
    return render(request, 'base/home.html', context)

def asset(request, pk):
    asset = Asset.objects.get(id=pk)
    context = {'asset' : asset}
    return render(request, 'base/asset.html', context)

def createAlarmAsset(request):
    form = AlarmAssetForm()

    # if request.method == 'POST':
    #     form = AlarmAssetForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')

    context = {'form': form}
    return render(request, 'base/alarm_asset_form.html', context)
