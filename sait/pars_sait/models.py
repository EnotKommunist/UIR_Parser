from django.db import models

# Create your models here.
class ParsInfo(models.Model):
    brand = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    id_seller = models.CharField(max_length=200)
    discounted_price = models.CharField(max_length=200)
    original_price = models.CharField(max_length=200)
    discount_percentage = models.CharField(max_length=200)
    product_rating = models.CharField(max_length=200)
    number_of_reviews = models.CharField(max_length=200)
    supplier = models.CharField(max_length=200)
    supplier_rating = models.CharField(max_length=200)
    link = models.CharField(max_length=200)


    def __str__(self):
        return f"{self.brand} {self.name}"
