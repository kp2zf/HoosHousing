from django.test import TestCase
from django.urls import reverse

from .utils import *

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
