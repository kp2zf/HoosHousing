'''
*  REFERENCES
*  Title: Generic editing views | Django documentation
*  Date: 2019-02-14
*  Availability: https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-editing/#formview
*
'''
from django import forms

from .models import Building
from .models import Review

class BuildingForm(forms.Form):
	name = forms.CharField()
	address = forms.CharField()

	def save_building(self):
		_name = self.cleaned_data['name']
		_addr = self.cleaned_data['address']
		Building(name=_name, address=_addr).save()

class ReviewForm(forms.ModelForm):
    rating_choices = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = forms.TypedChoiceField(choices=rating_choices, coerce=int)
    name = forms.CharField(label='Your name:', max_length=100)
    review_text = forms.CharField(label='Enter your review text:', max_length=1000)

    class Meta:
        model = Review
        fields = ('rating', 'name', 'review_text')

	# def save_review(self):
	# 	_name = self.cleaned_data['name']
	# 	_text = self.cleaned_data['review_text']
	# 	_rating = self.cleaned_data['rating']