from ..UndoRedoOperations.update_operation import UpdateOperation
from ..service.undo_redo_service import UndoRedoService

from typing import Callable

from ..serializers.car_serializer import CarSerializer
from ..serializers.card_serializer import CardSerializer
from ..serializers.transaction_serializer import TransactionSerializer

from ..models import Car, Card, Transaction

import copy

def update_undo_redo(function):
    def wrapper(*args, **kwargs):
        
        if "undoredo" not in kwargs or kwargs["undoredo"] is True:
            if "id" in kwargs:
                id = kwargs["id"]
            
            if "new_car" in kwargs:
                Serializer = CarSerializer
                old = Car.objects.get(id=id)
                new = kwargs["new_car"]
            elif "new_card" in kwargs:
                Serializer = CardSerializer
                old = Card.objects.get(id=id)
                new = kwargs["new_card"]
            elif "new_transaction" in kwargs:
                Serializer = TransactionSerializer
                old = Transaction.objects.get(id=id)
                new = kwargs["new_transaction"]
                                
            old = copy.deepcopy(old)
                            
            UndoRedoService.addUndoOperation(
                UpdateOperation(
                    old,
                    new,
                    Serializer
                )
            )
            UndoRedoService.clear_redo()
            
        return function(*args, **kwargs)
    
    return wrapper