from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('stocks/', views.ActiveStocksView.as_view(), name='active_stocks'),
]
