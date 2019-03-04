from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from .views import home
from . import views

app_name = 'housing'

urlpatterns = [
	# ex: /
	path('', home, name='index'),
	# ex: /add_building/
    path('add_building/', views.AddBuildingView.as_view(), name='add_building'),
    # ex: /buildings/3/
    path('buildings/<int:pk>/', views.building_detail, name='building_detail'),
    # ex: /buildings/add_unit/3/
	path('buildings/add_unit/<int:pk>/', views.AddUnitView.as_view(), name='add_unit'),
    # ex: /buildings/3/add_review/
    path('buildings/<int:pk>/add_review/', views.add_review, name='add_review'),
]

