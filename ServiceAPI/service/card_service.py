from ..serializers.card_serializer import CardSerializer
from ..models.card import Card
from ..utility.date_and_time import random_date

from random import randint, choice
from datetime import date


class CardService:
    def getAll():
        return Card.objects.all()

    def getAllDecreasingByDiscount():
        return Card.objects.order_by('-total_discounts')

    def get(id):
        try:
            card = Card.objects.get(id=id)
        except Card.DoesNotExist as e:
            raise Card.DoesNotExist(f'Error: {str(e)}')

        return card

    def create(card: Card):
        card.save()
        return card

    def createRandom(n):
        possible_first_names = [
            "Mike", "Ben", "Nick", "Lika", "Drew", "Dixie", "Yuri",
            "Hugh", "John", "Daniel", "Stephan", "Lucian", "Wilma",
            "Dixon B."
        ]

        possible_last_names = [
            "Oksmaul", "Dover", "Gurr", "Madiq", "Normous", "Oxbrown",
            "Nator", "Hawk", "G. Rection", "Roch", "Fingerdoo",
            "Tweenerlegs"
        ]

        cards = []
        for i in range(n):
            cards.append(CardService.create(Card(
                first_name=choice(possible_first_names),
                last_name=choice(possible_last_names),
                cnp=randint(1_000_000_000_000, 9_999_999_999_999),
                birthday=random_date(
                    date(1980, 1, 1), date(2003, 1, 1)
                ),
                registration_date=random_date(
                    date(2010, 1, 1), date(2022, 1, 1)
                )
            )))

        return cards

    def update(new_card, id):
        try:
            card = Card.objects.get(id=id)
        except Card.DoesNotExist as e:
            raise Card.DoesNotExist(f'Error: {str(e)}')

        card.first_name = new_card.first_name
        card.last_name = new_card.last_name
        card.cnp = new_card.cnp
        card.birthday = new_card.birthday
        card.registration_date = new_card.registration_date
        card.total_discounts = new_card.total_discounts

        card.save()

        return card

    def delete(id):
        try:
            card = Card.objects.get(id=id).delete()
        except Card.DoesNotExist as e:
            raise Card.DoesNotExist(f'Error: {str(e)}')

        return True
