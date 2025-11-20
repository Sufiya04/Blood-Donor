from django.urls import path
from .views import *

urlpatterns=[
    path('home',home, name='home'),
    path('donor', donor, name='donor'),
    path('request', recipient, name='recipient'),
    path('dashboard', dashboard, name='dashboard'),
    path('approve/<int:id>', approve, name='approve'),
    path('donorlist', donorlist, name='donorlist'),
    path('blood', blood, name='blood'),
    path('approved', approved, name='approved'),
    path('pending', pending, name='pending'),
    path('units', units, name='units'),
    path('admin', admin_login, name='admin'),
    path('signin', admin_signin, name='signin'),
    path('logout', admin_logout, name='logout'),
    path('reset', reset, name='reset')
]