from ..serializers.transaction_serializer import TransactionSerializer
from ..models.transaction import Transaction
from ..utility.date_and_time import random_datetime

from datetime import datetime
from random import randint, choice
from decimal import Decimal


class TransactionService:
    def getAll():
        return Transaction.objects.all()

    def get(id):
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoesNotExist as e:
            raise Transaction.DoesNotExist(f'Error: {str(e)}')

        return transaction

    def getBetweenSums(start: float, end: float):

        # start < components + workmansip < end
        # start - workmansip < components < end - workmansip

        from django.db.models import F

        transactions = Transaction.objects.filter(
            components_price__gte=start-F('workmanship'),
            components_price__lte=end-F('workmanship')
        )

        return transactions

    def create(transaction: Transaction):
        from car.models import Car
        from card.models import Card

        # components price is 0 if the card has warranty
        car = transaction.car

        if car.warranty:
            transaction.components_price = 0

        # 10% discount for workmanship if the client has a card
        card = transaction.card

        if card is not None:
            workmanship = float(transaction.workmanship)
            workmanship *= 0.9
            car.total_workmanship += Decimal(workmanship)
            car.save()

            discount = workmanship * 0.1
            card.total_discounts += Decimal(discount)
            card.save()

            transaction.workmanship = str(round(workmanship, 2))

        transaction.save()

        return transaction

    def createRandom(n):
        from car.models import Car
        from card.models import Card

        possible_cars = list(
            Car.objects.all())
        possible_cards = list(
            Card.objects.all())

        if len(possible_cards) == 0:
            possible_cards = [None]
        if len(possible_cars) == 0:
            raise Car.DoesNotExist("Error: Can't create random transactions."
                                   "There are no cars.")

        transactions = []

        for i in range(n):
            transactions.append(TransactionService.create(Transaction(
                car=choice(possible_cars),
                card=choice([choice(possible_cards), None]),
                components_price=randint(20, 700) * 10,
                workmanship=randint(200, 2500),
                datetime=random_datetime(
                    datetime(2001, 10, 1), datetime(2021, 12, 25))
            )))

        return transactions

    def update(new_transaction, id):
        try:
            transaction = Transaction.objects.get(id=id)
        except Transaction.DoestNotExist as e:
            raise Transaction.DoesNotExist(f'Error: {str(e)}')

        transaction.car = new_transaction.car
        transaction.card = new_transaction.card
        transaction.components_price = new_transaction.components_price
        transaction.workmanship = new_transaction.workmanship
        transaction.datetime = new_transaction.datetime

        transaction.save()

        return transaction

    def delete(id):
        try:
            Transaction.objects.get(id=id).delete()
        except Transaction.DoestNotExist as e:
            raise Transaction.DoesNotExist(f'Error: {str(e)}')

        return True

    def deleteBetweenDates(start, end):
        transactions = Transaction.objects.filter(
            datetime__gte=start,
            datetime__lte=end
        ).delete()

        return True
