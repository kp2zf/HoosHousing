from django.contrib import admin

from .models import Building, Unit, Review

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name','address']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['num_bedrooms']
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['building', 'rating', 'name', 'review_text', 'date']
