from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Asset, AlarmAsset, AssetPriceHistory
from .forms import AlarmAssetForm, AlarmAssetDefinedForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from bs4 import BeautifulSoup
from lxml import html
import requests
import re


# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password does not exist!')

    context = {
        'page': page
    }

    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user          = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {
        'form': form
    }

    return render(request, 'base/login_register.html', context)


@login_required(login_url='login')
def dashboard(request):
    q_asset            = request.GET.get('q_asset') if request.GET.get('q_asset') != None else ''
    assets       = Asset.objects.filter(Q(company_name__icontains=q_asset) | Q(ticker__icontains=q_asset))

    q_alarm            = request.GET.get('q_alarm') if request.GET.get('q_alarm') != None else ''
    alarms       = AlarmAsset.objects.filter(asset__ticker__icontains=q_alarm)

    deletar = request.GET.get('deletar') if request.GET.get('deletar') != None else ''
    if request.method == 'POST':
        print(deletar)
        alarm = AlarmAsset.objects.get(asset__ticker__contains=deletar)
        alarm.delete()
        return redirect('dashboard')

    context      = {
        'q_asset': q_asset,
        'q_alarm': q_alarm,
        'assets': assets,
        'alarms': alarms,
        }

    return render(request, 'base/dashboard.html', context)


def asset(request, ticker):
    asset          = Asset.objects.get(ticker=ticker)
    tick_nonumber  = re.sub(r'[0-9]', '', asset.ticker)
    img_url        = f'https://www.ivalor.com.br/media/emp/logos/{tick_nonumber}.png'
    response = requests.get(f'https://www.google.com/finance/quote/{asset}:BVMF?hl=pt')
    if response.status_code == 200:
        soup    = BeautifulSoup(response.text, "html.parser")
        price   = soup.find('div', {'class': 'YMlKec fxKbKc'})

    form = AlarmAssetDefinedForm()
    alarm          = AlarmAsset.objects.filter(asset=asset)

    price_historys = AssetPriceHistory.objects.all()

    if request.method == 'POST':
        form = AlarmAssetDefinedForm(request.POST)
        if form.is_valid():
            alarm      = form.save(commit=False)
            alarm.asset = asset
            alarm.user = request.user
            alarm.save()
            return redirect('dashboard')

    context        = {
        'form': form,
        'asset': asset,
        'alarm': alarm,
        'img_url': img_url,
        'price_historys': price_historys
        }


    return render(request, 'base/asset.html', context)


@login_required(login_url='login')
def alarmAsset(request, ticker):
    asset          = Asset.objects.get(ticker=ticker)
    tick_nonumber  = re.sub(r'[0-9]', '', asset.ticker)
    img_url        = f'https://www.ivalor.com.br/media/emp/logos/{tick_nonumber}.png'
    response = requests.get(f'https://www.google.com/finance/quote/{asset}:BVMF?hl=pt')
    soup    = BeautifulSoup(response.text, "html.parser")
    price   = soup.find('div', {'class': 'YMlKec fxKbKc'}) if response.status_code == 200 else ''
    print(price.text)
    form = AlarmAssetDefinedForm()
    alarm          = AlarmAsset.objects.filter(asset=asset)

    price_historys = AssetPriceHistory.objects.all()

    if request.method == 'POST':
        form = AlarmAssetDefinedForm(request.POST)
        if form.is_valid():
            alarm      = form.save(commit=False)
            alarm.asset = asset
            alarm.user = request.user
            alarm.save()
            return redirect('dashboard')

    context        = {
        'form': form,
        'asset': asset,
        'price': price.text,
        'alarm': alarm,
        'img_url': img_url,
        'price_historys': price_historys
        }


    return render(request, 'base/alarm_asset.html', context)

def createAlarmAsset(request):
    form   = AlarmAssetForm()
    assets = Asset.objects.all()

    if request.method == 'POST':
        form = AlarmAssetForm(request.POST)
        if form.is_valid():
            alarm      = form.save(commit=False)
            alarm.user = request.user
            alarm.save()
            return redirect('dashboard')

    context = {
        'form': form,
        'assets': assets
        }
    return render(request, 'base/alarm_asset_form.html', context)


def createAlarmAssetDefined(request, ticker):
    form   = AlarmAssetDefinedForm()
    asset = Asset.objects.get(ticker=ticker)
    alarm = AlarmAsset()

    if request.method == 'POST':
        form = AlarmAssetDefinedForm(request.POST)
        if form.is_valid():
            alarm      = form.save(commit=False)
            alarm.asset = asset
            alarm.user = request.user
            alarm.save()
            return redirect('dashboard')

    context = {
        'form': form,
        'asset': asset
        }
    return render(request, 'base/alarm_asset_form.html', context)

@login_required(login_url='login')
def updateAlarmAsset(request, pk):
    alarm = AlarmAsset.objects.get(id=pk)
    form  = AlarmAssetDefinedForm()

    if request.method == 'POST':
        form = AlarmAssetForm(request.POST)
        if form.is_valid():
            alarm      = form.save(commit=False)
            alarm.asset = asset
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'base/alarm_asset_form.html', context)


def deleteAlarmAsset(request, pk):
    alarm = AlarmAsset.objects.get(id=pk)
    if request.method == 'POST':
        alarm.delete()
        return redirect('dashboard')
    return render(request, 'base/delete_alarm.html')
