from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=50, default='Unknown')
    description = models.TextField(max_length=200, null=True)
    #__str__método para imprimir un objeto de marca de automóvil
    def __str__(self):
        return self.name 


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)  
    name = models.CharField( max_length=50, default='')
    dealer_id = models.IntegerField(default=1)        
    type_c = models.CharField(max_length=20, choices=(('Sedan', 'Sedan',), ('SUV', 'SUV'), ('HATCHBACK', 'HATCHBACK'),('WAGON', 'WAGON')))
    year = models.DateTimeField(null=True)
    def __str__(self):
        return self.name
   



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
