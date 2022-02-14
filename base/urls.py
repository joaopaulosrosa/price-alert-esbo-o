from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('asset/<str:ticker>/', views.asset, name="asset"),

    path('alarm-asset/<str:pk>/', views.alarmAsset, name="alarm-asset"),
    path('create-alarm-asset/', views.createAlarmAsset, name="create-alarm-asset"),
]
