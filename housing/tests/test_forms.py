from django.test import TestCase
from django.forms import ValidationError

from housing.forms import BuildingForm, ReviewForm, UnitForm

from .utils import *

''' Begin forms test cases. '''

class BuildingFormTest(TestCase):

	def test_valid_data(self):
		name = 'Wertland Square'
		addr = '214 14th. St. NW, Charlottesville, VA 22903'
		form = BuildingForm({
			'name': name,
			'address': addr,
			'admin': 'jm8wx',
			'neighborhood': 'Rugby Road'
	    })
		self.assertTrue(form.is_valid())
		building = form.save()
		self.assertEqual(building.name, name)
		self.assertEqual(building.address, addr)

	def test_blank_data(self):
	    self.maxDiff =None
	    form = BuildingForm({})
	    self.assertFalse(form.is_valid())
	    self.assertIsNotNone(form.errors)

class UnitFormTest(TestCase):

	def test_valid_data(self):
		monthly_rent = 9000
		square_footage = 1400
		num_bedrooms = 11
		available = True
		form = UnitForm({
			'monthly_rent': monthly_rent,
			'square_footage': square_footage,
			'num_bedrooms': num_bedrooms,
			'available': available
	    })
		self.assertTrue(form.is_valid())
		building = create_building()
		building.save() # Django requires this since there is a relation
		unit = form.save(building)
		self.assertEqual(unit.monthly_rent, monthly_rent)
		self.assertEqual(unit.square_footage, square_footage)
		self.assertEqual(unit.num_bedrooms, num_bedrooms)
		self.assertEqual(unit.available, available)

	def test_blank_data(self):
	    form = UnitForm({})
	    self.assertFalse(form.is_valid())
	    self.assertEqual(form.errors, {
	        'monthly_rent': ['This field is required.'],
	        'square_footage': ['This field is required.'],
	        'num_bedrooms': ['This field is required.'],
	    })

class ReviewFormTest(TestCase):

	def test_valid_data(self):
		name = 'Mr. Rogers'
		rating = 1
		review_text = 'This building is full of rats!'
		form = ReviewForm({
			'name': name,
			'rating': rating,
			'review_text': review_text
	    })
		self.assertTrue(form.is_valid())
		building = create_building()
		building.save() # Django requires this since there is a relation
		review = form.save(building)
		self.assertEqual(review.building, building)
		self.assertEqual(review.name, name)
		self.assertEqual(review.rating, rating)
		self.assertEqual(review.review_text, review_text)
		self.assertIsNotNone(review.date)

	def test_blank_data(self):
	    form = UnitForm({})
	    self.assertFalse(form.is_valid())
	    self.assertEqual(form.errors, {
	        'monthly_rent': ['This field is required.'],
	        'square_footage': ['This field is required.'],
	        'num_bedrooms': ['This field is required.'],
	    })
