from django.conf.urls import url
from django.contrib import admin

from listings import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^listings/(\d+)/', views.listing_detail, name='listing_detail'),
]
