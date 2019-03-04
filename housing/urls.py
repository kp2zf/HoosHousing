from django.urls import path

from . import views

app_name = 'housing'

urlpatterns = [
	# ex: /
	path('', views.home, name='index'),
	# ex: /add_building/
    path('add_building/', views.AddBuildingView.as_view(), name='add_building'),
    # ex: /buildings/3/
    path('buildings/<int:pk>/', views.building_detail, name='building_detail'),

	path('buildings/add_unit', views.AddUnitView.as_view(), name='add_unit')
]
