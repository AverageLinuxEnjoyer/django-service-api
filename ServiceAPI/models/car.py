from django.db import models


class Car(models.Model):
    model = models.CharField(max_length=50)
    acquisition_date = models.DateField()
    kilometers = models.DecimalField(decimal_places=2, max_digits=10)
    warranty = models.BooleanField()
    total_workmanship = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0
    )
