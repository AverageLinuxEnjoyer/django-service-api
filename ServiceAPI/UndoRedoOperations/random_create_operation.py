from django.db import models
from .undo_redo_operation import UndoRedoOperation


class RandomCreateOperation(UndoRedoOperation):
    def __init__(self, added_entities):
        self.entities = []
        
        for entity in added_entities:
            self.entities.append([entity, entity.pk])

    def undo(self):
        for entity in self.entities:
            entity[0].delete()

    def redo(self):
        for entity in self.entities:
            entity[0].pk = entity[1]
            entity[0].save()
        