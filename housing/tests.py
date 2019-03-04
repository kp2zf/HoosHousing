from django.urls import reverse
from django.test import TestCase

from .models import Building

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
	def test_future_question(self):
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

''' Helper methods for tests. '''

def create_building():
	return Building(
		name='Grandmarc', 
		address='301 15th St NW, Charlottesville, VA 22903'
	)
