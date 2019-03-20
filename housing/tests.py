from django.urls import reverse
from django.test import TestCase

from .models import Building, Unit

''' Begin models test cases. '''

class ModelTests(TestCase):
	def test_building_exists(self):
		building = create_building()
		self.assertIsNotNone(building)

''' Begin forms test cases. '''

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
		self.assertContains(response, "maps.google.com/maps")
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
