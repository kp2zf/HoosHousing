from django.contrib import admin

from .models import Building
from .models import Review


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name','address']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['building', 'rating', 'name', 'review_text', 'date']