from django.db import models
from .undo_redo_operation import UndoRedoOperation


class CreateOperation(UndoRedoOperation):

    def __init__(self, added_entity: models.Model):
        self.added_entity = added_entity
        self.pk = added_entity.pk

    def undo(self):
        self.added_entity.delete()

    def redo(self):
        self.added_entity.pk = self.pk
        self.added_entity.save()
        