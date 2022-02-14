import re
from django.shortcuts import render, redirect
from django.db.models import Q
import requests
from .models import Asset, AlarmAsset
from .forms import AlarmAssetForm

# Create your views here.

def home(request):
    alarms  = AlarmAsset.objects.all()
    q       = request.GET.get('q') if request.GET.get('q') != None else ''
    assets  = Asset.objects.filter(Q(company_name__icontains=q) | Q(ticker__icontains=q)
    )
    context = {
        'assets': assets,
        'alarms': alarms,
        # 'form': form
        }

    return render(request, 'base/home.html', context)


def asset(request, ticker):
    asset         = Asset.objects.get(ticker=ticker)
    data_getter   = f'results.{ticker}'
    tick_nonumber = re.sub(r'[0-9]', '', asset.ticker)
    img_url       = f'https://www.ivalor.com.br/media/emp/logos/{tick_nonumber}.png'
    response      = requests.get(f'https://api.hgbrasil.com/finance/stock_price?key=3ebed24b&symbol={asset}').json()['results'][asset.ticker]
    context       = {
        'asset' : asset,
        'img_url': img_url,
        'data_getter': data_getter,
        'response': response
        }

    return render(request, 'base/asset.html', context)


def alarmAsset(request, pk):
    form        = AlarmAssetForm()
    alarm_asset = AlarmAsset.objects.get(id=pk)
    context     = {
        'alarm_asset' : alarm_asset,
        'form': form
        }
    return render(request, 'base/alarm_asset.html', context)


def createAlarmAsset(request):
    form = AlarmAssetForm()

    if request.method == 'POST':
        form = AlarmAssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/alarm_asset_form.html', context)
