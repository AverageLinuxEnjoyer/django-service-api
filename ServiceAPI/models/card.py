from django.db import models
from django.core.validators import RegexValidator


class Card(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cnp = models.CharField(
        max_length=13,
        validators=[RegexValidator(
            regex=r'^[0-9]{13}$',
            message='CNP-ul trebuie sa aiba lungimea 13'
                    'si sa fie format din cifre.',
            code='nomatch'
        )],
        unique=True
    )
    birthday = models.DateField()
    registration_date = models.DateField()
    total_discounts = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0
    )
