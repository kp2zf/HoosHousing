from django.db import models

#apartment complex
class Listing(models.Model):
    price = models.IntegerField()
    complex_name = models.CharField(max_length=100)
    units = models.ManyToManyField('Unit')

#unit e.i. 4 room $3000, 3 room $2000 etc
class Unit(models.Model):
    overall_price = models.IntegerField()
    price_per_unit = models.IntegerField()
    squarefootage = models.IntegerField()
    num_rooms = models.IntegerField()

    def __str__(self):
        return str(self.num_rooms)