from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from .views import home
from . import views
from django.contrib.auth import logout
app_name = 'housing'

urlpatterns = [
    path('admin/', admin.site.urls),
	# ex: /
	path('', home, name='index'),
    # ex: /review/
    path('review/', views.review, name='review'),
    # ex: /search/
    path('search/', views.SearchView.as_view(), name='search'),
    # ex: /advanced_search/
    path('advanced_search/', views.AdvancedSearchView.as_view(), name='advanced_search'),
    # ex: /search_form/
    path('search_form/', views.search, name='search_form'),
    # ex: /advanced_search_form/
    path('advanced_search_form/', views.advanced_search, name='advanced_search_form'),
    # ex: /toggle_building_published/
    path('toggle_building_published/<int:pk>/', views.toggle_building_published, name='toggle_building_published'),
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
    # upvote review path
    path('buildings/<int:pk>/<str:reviewer_name>/<str:voter_name>/<slug:sorting>/vote/', views.helpful_vote, name='helpful_vote'),
    # sorted review path
    path('buildings/<int:pk>/<slug:sorting>/', views.building_detail, name='building_detail'),
    path('edit/<int:pk>/',views.EditBuilding.as_view(),name="edit_building"),
    path('myFavorites/', views.myFavorites, name='myFavorites'),
    path('myReviews/', views.myReviews, name='myReviews'),
    path('logout/', views.my_logout, name="logout"),
    path('buildings/<int:pk>/favorite', views.favoriteBuilding, name='favoriteBuilding'),
    path('success/',views.SuccessView.as_view(),name="success"),
]


# for serving static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
