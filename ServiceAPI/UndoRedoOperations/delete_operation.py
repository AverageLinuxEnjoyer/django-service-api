from django.db import models
from .undo_redo_operation import UndoRedoOperation


class DeleteOperation(UndoRedoOperation):
    def __init__(self, deleted_entity: models.Model):
        self.deleted_entity = deleted_entity
        self.pk = deleted_entity.pk

    def undo(self):
        self.deleted_entity.save()

    def redo(self):
        self.deleted_entity.delete()
