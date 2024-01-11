from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}: {self.description}"

class CarModel(models.Model):
    CarType = enumerate(["Sedan", "SUV", "WAGON"])
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dealer_id = models.IntegerField()
    car_type = models.IntegerField(choices=CarType)
    year = models.DateField()
    def __str__(self):
        return f"{self.name} {self.car_type} {self.year}"

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
