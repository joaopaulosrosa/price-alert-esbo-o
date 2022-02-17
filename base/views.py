from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Asset, AlarmAsset, AssetPriceHistory
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import AlarmAssetForm
from django.db.models import Q
import requests
import re


# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

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
            return redirect('home')
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
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {
        'form': form
    }

    return render(request, 'base/login_register.html', context)


def home(request):
    if request.user.is_authenticated:
        alarms = AlarmAsset.objects.filter(user=request.user)
    q            = request.GET.get('q') if request.GET.get('q') != None else ''
    assets       = Asset.objects.filter(Q(company_name__icontains=q) | Q(ticker__icontains=q))
    context      = {
        'assets': assets,
        'alarms': alarms,
        }

    return render(request, 'base/home.html', context)


def asset(request, ticker):
    asset         = Asset.objects.get(ticker=ticker)
    # data_getter   = f'results.{ticker}'
    # tick_nonumber = re.sub(r'[0-9]', '', asset.ticker)
    # img_url       = f'https://www.ivalor.com.br/media/emp/logos/{tick_nonumber}.png'
    price_historys = AssetPriceHistory.objects.all()
    context       = {
        'asset' : asset,
        # 'img_url': img_url,
        # 'data_getter': data_getter,
        'price_historys': price_historys
        }

    return render(request, 'base/asset.html', context)


@login_required(login_url='login')
def alarmAsset(request, pk):
    form        = AlarmAssetForm()
    alarm_asset = AlarmAsset.objects.get(id=pk)
    context     = {
        'alarm_asset' : alarm_asset,
        'form': form
        }
    return render(request, 'base/alarm_asset.html', context)

@login_required(login_url='login')
def createAlarmAsset(request):
    form = AlarmAssetForm()
    assets = Asset.objects.all()

    if request.method == 'POST':
        form = AlarmAssetForm(request.POST)
        if form.is_valid():
            alarm = form.save(commit=False)
            alarm.user = request.user
            alarm.save()
            return redirect('home')

    context = {
        'form': form,
        'assets': assets
        }
    return render(request, 'base/alarm_asset_form.html', context)

@login_required(login_url='login')
def updateAlarmAsset(request, pk):
    alarm = AlarmAsset.objects.get(id=pk)
    form = AlarmAssetForm(instance=alarm)

    if request.method == 'POST':
        form = AlarmAssetForm(request.POST, instance=alarm)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/alarm_asset_form.html', context)
