from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from .views import home
from . import views

app_name = 'housing'

urlpatterns = [
	# ex: /
	path('', views.home, name='index'),
	# ex: /add_building/
    path('add_building/', views.AddBuildingView.as_view(), name='add_building'),
    # ex: /buildings/3/
    path('buildings/<int:pk>/', views.building_detail, name='building_detail'),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here
    url(r'^$', home, name='home'),
]