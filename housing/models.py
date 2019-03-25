from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey

from multiselectfield import MultiSelectField


''' Validators. '''

def validate_review_rating(value):
    ''' Make sure Review rating is 1, 2, 3, 4, or 5. '''
    if value not in range(1,6):
        raise ValidationError(
            _('%(value)s is not an integer from 1 to 5'),
            params={'value': value},
        )

''' Model classes. '''

MY_CHOICES=(('Jefferson Park Avenue','Jefferson Park Avenue'),
            ('Corner','Corner'),
            ('Rugby Road','Rugby Road'),
            ('West Main','West Main'))
# A Building is normally an apartment or housing complex. Each
# Building contains one or more Units.
class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images/')

    neighborhood = MultiSelectField(choices=MY_CHOICES, null=True)
    def __str__(self):
        return '{} ({})'.format(self.name, self.address)

# Each Unit represents a subsection of a Building that is rentable.
# The monthly rent of a Unit represents the total rent in US Dollars
# for one month.
class Unit(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    monthly_rent = models.IntegerField()
    square_footage = models.IntegerField()
    num_bedrooms = models.IntegerField()
    available = models.BooleanField()

    def __str__(self):
        return 'Rent: {} Bedrooms: {} '.format(self.monthly_rent, self.num_bedrooms)

# Each review contains the name of the reviewer, a numerical rating out of 5, the text of the review, and the building
# for which it applies
class Review(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField('date published')
    rating = models.IntegerField(validators = [validate_review_rating]) #the user's rating (out of 5 stars) of the apartment
    helpful_score = models.IntegerField(default=0) #amount of users that found this review helpful
    review_text = models.TextField()
