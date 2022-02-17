from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('asset/<str:ticker>/', views.asset, name="asset"),

    path('alarm-asset/<str:pk>/', views.alarmAsset, name="alarm-asset"),
    path('update-asset/<str:pk>/', views.updateAlarmAsset, name="update-alarm-asset"),
    path('create-alarm-asset/', views.createAlarmAsset, name="create-alarm-asset"),
]
