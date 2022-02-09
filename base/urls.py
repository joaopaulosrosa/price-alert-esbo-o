from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('asset/<str:pk>/', views.asset, name="asset"),

    path('create-alarm-asset/', views.createAlarmAsset, name="create-alarm-asset"),
]
