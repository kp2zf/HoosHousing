'''
*  REFERENCES
*  Title: Generic editing views | Django documentation
*  Date: 2019-02-14
*  Availability: https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-editing/#formview
*
'''
from django import forms

from .models import Building

class BuildingForm(forms.Form):
	name = forms.CharField()
	address = forms.CharField()

	def save_building(self):
		_name = self.cleaned_data['name']
		_addr = self.cleaned_data['address']
		Building(name=_name, address=_addr).save()

class BuildingImageForm(forms.Form):
	image = forms.ImageField()

	def save_building(self, building):
		print('saving image', self.cleaned_data['image'])
		building.image = self.cleaned_data['image']
		building.save()