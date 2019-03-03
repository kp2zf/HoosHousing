from django.db import models

# A Building is normally an apartment or housing complex. Each
# Building contains one or more Units.
class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)

    def __str__(self):
        return '{} ({})'.format(name, address)

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
        return str(self.num_rooms)