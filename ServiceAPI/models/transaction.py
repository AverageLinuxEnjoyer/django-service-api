from django.db import models
from .car import Car
from .card import Card


class Transaction(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    components_price = models.DecimalField(decimal_places=2, max_digits=10)
    workmanship = models.DecimalField(decimal_places=2, max_digits=10)
    datetime = models.DateTimeField()
