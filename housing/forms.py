'''
*  REFERENCES
*  Title: Generic editing views | Django documentation
*  Date: 2019-02-14
*  Availability: https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-editing/#formview
*
'''
from django import forms
from django.utils import timezone
from .models import Building, Review, Unit
from multiselectfield import MultiSelectField

MY_CHOICES=(('Jefferson Park Avenue','Jefferson Park Avenue'),
			('Corner','Corner'),
			('Rugby Road','Rugby Road'),
			('West Main','West Main'))

class BuildingForm(forms.Form):
	name = forms.CharField()
	address = forms.CharField()
	neighborhood=forms.ChoiceField(choices=MY_CHOICES)
	admin=forms.CharField(required=False,widget=forms.HiddenInput())
	is_approved = forms.BooleanField(required=False,widget=forms.HiddenInput())

	pet_allowed= forms.BooleanField(required=False)
	is_furnished=forms.BooleanField(required=False)
	air_conditioning=forms.BooleanField(required=False)
	lease_length=forms.CharField(max_length=100)
	parking_cost=forms.IntegerField(required=False)
	pool=forms.BooleanField(required=False)
	gym=forms.BooleanField(required=False)
	website_link=forms.CharField(max_length=100,required=False)
	email=forms.CharField(max_length=100,required=False)
	phone_number=forms.CharField(max_length=100,required=False)

	def save(self,admin):
		_name = self.cleaned_data['name']
		_addr = self.cleaned_data['address']
		_neighborhood = self.cleaned_data['neighborhood']
		_admin = admin
		_pet_allowed=self.cleaned_data['pet_allowed']
		_is_furnished=self.cleaned_data['is_furnished']
		_air_conditioning=self.cleaned_data['air_conditioning']
		_lease_length=self.cleaned_data['lease_length']
		_parking_cost=self.cleaned_data['parking_cost']
		_pool=self.cleaned_data['pool']
		_gym=self.cleaned_data['gym']
		_website_link=self.cleaned_data['website_link']
		_email=self.cleaned_data['email']
		_phone_number=self.cleaned_data['phone_number']

		is_approved=False
		building = Building(admin=_admin,name=_name, address=_addr,neighborhood=_neighborhood,pet_allowed=_pet_allowed,
		is_furnished=_is_furnished,air_conditioning=_air_conditioning,lease_length=_lease_length,parking_cost=_parking_cost,
		pool=_pool,gym=_gym,website_link=_website_link,email=_email,phone_number=_phone_number)
		building.save()
		return building

class BuildingImageForm(forms.Form):
	image = forms.ImageField()

	def save(self, building):
		building.image = self.cleaned_data['image']
		building.save()
		return building

class UnitForm(forms.Form):
	monthly_rent = forms.IntegerField()
	square_footage = forms.IntegerField()
	num_bedrooms = forms.IntegerField()
	available = forms.BooleanField(required=False)

	def save(self, building):
		_building = building
		_monthly_rent = self.cleaned_data['monthly_rent']
		_square_footage = self.cleaned_data['square_footage']
		_num_bedrooms = self.cleaned_data['num_bedrooms']
		_available = self.cleaned_data['available']

		unit = Unit(building = _building, monthly_rent=_monthly_rent, square_footage=_square_footage, num_bedrooms=_num_bedrooms, available=_available)
		unit.save()
		return unit

class ReviewForm(forms.Form):
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

	def save(self, building):
		name = self.cleaned_data['name']
		rating = self.cleaned_data['rating']
		review_text = self.cleaned_data['review_text']
		review = Review(building=building, rating=rating, name=name, review_text=review_text)
		review.date = timezone.now()
		review.save()
		return review

class UpdateForm(forms.Form):
	address=forms.CharField(max_length=100)


