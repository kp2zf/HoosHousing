from django.db import models
from django.urls import reverse

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

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
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    pet_allowed= models.BooleanField()
    is_furnished=models.BooleanField()
    air_conditioning=models.BooleanField()
    lease_length=models.IntegerField()
    parking=models.BooleanField(null=True)
    pool=models.BooleanField()
    gym=models.BooleanField()
    neighborhood = MultiSelectField(choices=MY_CHOICES, null=True)
    website_link=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=100)
    approved = models.BooleanField(null=True, blank=True)
    admin = models.CharField(max_length=100,null=True, blank=True)
    favorites = models.ManyToManyField(User, blank=True)
    rating=models.DecimalField(null=True,max_digits=3,decimal_places=2)
    def __str__(self):
        return '{} ({})'.format(self.name, self.address)

    def get_absolute_url(self):
    	return reverse('housing:building_detail', kwargs={'pk': self.id })

# Each Unit represents a subsection of a Building that is rentable.
# The monthly rent of a Unit represents the total rent in US Dollars
# for one month.
class Unit(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
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
    header = models.CharField(max_length=100)
    review_text = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Vote(models.Model):
    # building = models.ForeignKey(Building, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
