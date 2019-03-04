from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from .views import home
from . import views

app_name = 'housing'

urlpatterns = [
    path('listing_page/',views.search,name="search"),
    path('admin/', admin.site.urls),
	# ex: /
	path('', home, name='index'),
	# ex: /add_building/
    path('add_building/', views.AddBuildingView.as_view(), name='add_building'),
    # ex: /buildings/3/
    path('buildings/<int:pk>/', views.building_detail, name='building_detail'),
    # ex: /upload_building_image/
    path('upload_building_image/<int:pk>/', views.upload_building_image, name='upload_building_image'),
    # ex: /buildings/add_unit/3/
    path('buildings/add_unit/<int:pk>/', views.AddUnitView.as_view(), name='add_unit'),
    # ex: /buildings/3/add_review/
    path('buildings/<int:pk>/add_review/', views.add_review, name='add_review'),
]


# for serving static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)