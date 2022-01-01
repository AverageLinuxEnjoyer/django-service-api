from ..serializers.card_serializer import CardSerializer
from ..models.card import Card
from ..utility.date_and_time import random_date

from .undo_redo_service import UndoRedoService

from ..UndoRedoDecorators.create_decorator import create_undo_redo
from ..UndoRedoDecorators.update_decorator import update_undo_redo

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
    
    def search(text: str):
        from django.db.models import Q
        cards = Card.objects.filter(
            Q(first_name__icontains=text) |
            Q(last_name__icontains=text) |
            Q(cnp__icontains=text) |
            Q(birthday__icontains=text) |
            Q(registration_date__icontains=text) |
            Q(total_discounts__icontains=text)
        )
        
        return cards

    @create_undo_redo
    def create(card: Card, undoredo: bool = True):
        card.save()
        return card

    def createRandom(n, undoredo: bool = True):
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
            ), undoredo=False))

        return cards

    @update_undo_redo
    def update(new_card, id, undoredo: bool = True):
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

    def delete(id, undoredo: bool = True):
        import copy
        try:
            card = Card.objects.get(id=id)
            card_copy = copy.deepcopy(card)
            
            card.delete()
            
        except Card.DoesNotExist as e:
            raise Card.DoesNotExist(f'Error: {str(e)}')

        return card_copy
