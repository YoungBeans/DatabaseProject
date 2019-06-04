"""team URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='search'),
    path('result/<pk>/', views.result, name='result'),
    path('favorite/<pk>/', views.favorite, name='favorite'),
    path('delFavorite/<pk>/', views.delFavorite, name='delFavorite'),
    path('addRate/', views.addRate, name='addRate'),
    path('searching/', views.searching, name='searching'),
    path('searching2/', views.searching2, name='searching2'),
    path('foodSearch/', views.foodSearch, name='foodSearch'),
    path('foodSerched/<pk>/', views.foodSerched, name='foodSerched'),
    path('mostlook/', views.most_look, name="mostlook"),
    path('favouritelook/', views.most_favourite, name="favouritelook"),
]
