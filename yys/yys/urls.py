"""yys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from income_calculator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('events/', views.dummy, name='events'),
    path('event_entities/', views.dummy, name='event_entities'),
    path('event_groups/', views.dummy, name='event_groups'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('new_item/', views.new_item, name='new_item'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('item/<int:item_id>/delete', views.dummy, name='item_delete'),
    path('item/<int:item_id>/edit', views.dummy, name='item_edit'),
    path('periods/', views.dummy, name='periods'),
]
