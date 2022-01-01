from ..UndoRedoOperations.random_create_operation import RandomCreateOperation
from ..service.undo_redo_service import UndoRedoService

from typing import Callable


def random_create_undo_redo(function: Callable):
    def wrapper(*args, **kwargs):

        created_objects = function(*args, **kwargs)

        if "undoredo" not in kwargs or kwargs["undoredo"] is True:
            UndoRedoService.addUndoOperation(
                RandomCreateOperation(created_objects))
            UndoRedoService.clear_redo()

        return created_objects

    return wrapper
