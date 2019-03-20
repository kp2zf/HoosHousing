from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .forms import BuildingForm, ReviewForm, UnitForm
from .models import Building, Review, Unit

''' Begin models test cases. '''

class ModelTests(TestCase):
	def test_building_exists(self):
		building = create_building()
		self.assertIsNotNone(building)

	def test_unit_exists(self):
		building = create_building()
		unit = create_unit(building)
		self.assertIsNotNone(unit)

	def test_reviw_exists(self):
		building = create_building()
		review = create_review(building)
		self.assertIsNotNone(review)

''' Begin forms test cases. '''

class BuildingFormTest(TestCase):

	def test_valid_data(self):
		name = 'Wertland Square'
		addr = '214 14th. St. NW, Charlottesville, VA 22903'
		form = BuildingForm({
			'name': name,
			'address': addr
	    })
		self.assertTrue(form.is_valid())
		building = form.save()
		self.assertEqual(building.name, name)
		self.assertEqual(building.address, addr)

	def test_blank_data(self):
	    form = BuildingForm({})
	    self.assertFalse(form.is_valid())
	    self.assertEqual(form.errors, {
	        'name': ['This field is required.'],
	        'address': ['This field is required.'],
	    })



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

''' Begin views test cases. '''

class HomeTestCases(TestCase):
	def test_empty_home(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No buildings found')

class BuildingDetailViewTests(TestCase):
	def test_without_building(self):
		"""
		The detail view of a question with a pub_date in the future
		returns a 404 not found.
		"""
		url = reverse('housing:building_detail', args=(0,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_with_building(self):
		"""
		The detail view of a question with a pub_date in the future
		returns a 404 not found.
		"""
		building = create_building()
		building.save()
		url = reverse('housing:building_detail', args=(building.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, building.name)
		self.assertContains(response, building.address)
		self.assertContains(response, 'No units to show')

	def test_building_detail_view_with_unit(self):
		"""
		The detail view of a question with a pub_date in the future
		returns a 404 not found.
		"""
		building = create_building()
		building.save()
		unit = create_unit(building)
		unit.save()
		url = reverse('housing:building_detail', args=(building.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, building.name)
		self.assertContains(response, building.address)
		self.assertNotContains(response, 'No units to show')

''' Helper methods for tests. '''

def create_building():
	return Building(
		name='Grandmarc',
		address='301 15th St NW, Charlottesville, VA 22903'
	)

def create_unit(building):
	return Unit(
		building = building,
		monthly_rent = 850,
		square_footage = 800,
		num_bedrooms = 3,
		available = True,
	)

def create_review(building):
	return Review(
		building = building,
		name = 'Jack Morris',
		date = timezone.now(),
		rating = 2,
		review_text = 'This building is fine'
	)
