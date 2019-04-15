from django.utils import timezone

from housing.models import Building, Review, Unit

from random import random

''' Helper methods for tests. '''

def random_bool():
	return random() < 0.5

def create_building():
	return Building(
		name='Grandmarc',
		address='301 15th St NW, Charlottesville, VA 22903',
		pet_allowed=random_bool(),
		is_furnished=random_bool(),
		air_conditioning=random_bool(),
		lease_length=12,
		parking=random_bool(),
		pool=random_bool(),
		gym=random_bool(),
		website_link='http://www.grandmarc.edu',
		phone_number='8675309',
		approved=False,
		admin='jm8wx',
		rating=5
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
def create_high_review(building):
	return Review(
		building = building,
		name = 'Asa',
		date = timezone.now(),
		rating = 5,
		review_text = 'This building is fire'
	)
