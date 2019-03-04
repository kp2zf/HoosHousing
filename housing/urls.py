from django.urls import path
from django.contrib import admin


from . import views

app_name = 'housing'

urlpatterns = [
    path('listing_page/',views.search,name="search"),
    path('admin/', admin.site.urls),
	# ex: /
	path('', views.home, name='index'),
	# ex: /add_building/
    path('add_building/', views.AddBuildingView.as_view(), name='add_building'),
    # ex: /buildings/3/
    path('buildings/<int:pk>/', views.building_detail, name='building_detail')
]