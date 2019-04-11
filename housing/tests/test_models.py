from django.test import TestCase

from .utils import *


class ModelTests(TestCase):
	def test_building_exists(self):
		building = create_building()
		self.assertIsNotNone(building)

	def test_unit_exists(self):
		building = create_building()
		unit = create_unit(building)
		self.assertIsNotNone(unit)

	def test_review_exists(self):
		building = create_building()
		review = create_review(building)
		self.assertIsNotNone(review)
