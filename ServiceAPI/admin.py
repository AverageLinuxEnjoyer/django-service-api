from django.contrib import admin

# Register your models here.
from .models.car import Car
from .models.card import Card
from .models.transaction import Transaction

admin.site.register(Car)
admin.site.register(Card)
admin.site.register(Transaction)