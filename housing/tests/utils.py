from django.utils import timezone

from housing.models import Building, Review, Unit

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
