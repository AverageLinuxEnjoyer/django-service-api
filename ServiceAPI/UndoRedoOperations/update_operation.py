from django.db import models
from .undo_redo_operation import UndoRedoOperation

from ..serializers.car_serializer import CarSerializer
from ..serializers.card_serializer import CardSerializer
from ..serializers.transaction_serializer import TransactionSerializer

class UpdateOperation(UndoRedoOperation):

    def __init__(self, old: models.Model, new: models.Model, Serializer):
        self.pk = old.pk
        self.Serializer = Serializer
        self.old = self.Serializer(instance=old, many=False).data
        self.new = self.Serializer(instance=new, many=False).data

    def setService(self):
        from ..service.car_service import CarService
        from ..service.card_service import CardService
        from ..service.transaction_service import TransactionService
        
        if self.Serializer == CarSerializer:
            self.Service = CarService
        elif self.Serializer == CardSerializer:
            self.Service = CardService
        elif self.Serializer == TransactionSerializer:
            self.Service = TransactionService
        
    def undo(self):
        self.setService()
        
        serializer = self.Serializer(data=self.old)

        if serializer.is_valid():
            old_instance = serializer.create()
        
        self.Service.update(
            old_instance, 
            self.pk, 
            undoredo=False
        )

    def redo(self):
        self.setService()
        
        serializer = self.Serializer(data=self.new)

        if serializer.is_valid():
            new_instance = serializer.create()
        
        self.Service.update(
            new_instance, 
            self.pk, 
            undoredo=False
        )
