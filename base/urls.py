from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    # path('', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('asset/<str:ticker>/', views.asset, name="asset"),
    path('alarm-asset/<str:ticker>/', views.alarmAsset, name="alarm-asset"),

    path('create-alarm-asset/', views.createAlarmAsset, name="create-alarm-asset"),
    path('create-alarm-asset-defined/<str:ticker>/', views.createAlarmAssetDefined, name="create-alarm-asset-defined"),
    path('update-alarm/<str:pk>/', views.updateAlarmAsset, name="update-alarm-asset"),
    path('delete-alarm/<str:pk>/', views.deleteAlarmAsset, name="delete-alarm-asset"),
]
