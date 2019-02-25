from django.conf import settings
from django.conf.urls.static import static
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
    # ex: /upload_building_image/
    path('upload_building_image/<int:pk>/', views.upload_building_image, name='upload_building_image'),
]


# for serving static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)