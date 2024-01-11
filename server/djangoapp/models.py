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

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
