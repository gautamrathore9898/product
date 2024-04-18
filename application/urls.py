
from django.contrib import admin
from django.urls import path
from application.views import HomeView, ProductView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('insert', HomeView.as_view(), name='insert'),
    path('product/', ProductView.as_view(), name='product'),
    path('product/<int:pk>', ProductView.as_view(), name='product_id'),


]
