from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home , name='home'),
    path('us/<state>/<city>', views.city , name='city'),
    path('us/<state>/<city>/<business>', views.business , name='business'),
    path('us/<state>/<city>/<business>/<hash>', views.detail , name='detail'),
    path('contact', views.contact , name='contact'),
    path('about', views.about , name='about'),
    path('terms-and-conditions', views.tnc , name='tnc'),
    path('policy', views.policy , name='policy'),
    path('disclaimer', views.disclaimer , name='disclaimer'),

    # path('ponds/', views.getPrice, name = 'getPrice'),
    # path('quantity', views.getquantity, name='getquantity'),
]

