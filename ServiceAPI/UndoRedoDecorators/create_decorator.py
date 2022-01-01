from ..UndoRedoOperations.create_operation import CreateOperation
from ..service.undo_redo_service import UndoRedoService

from typing import Callable

def create_undo_redo(function: Callable):
    def wrapper(*args, **kwargs):
        
        created_object = function(*args, **kwargs)
        
        if "undoredo" not in kwargs or kwargs["undoredo"] is True:
            UndoRedoService.addUndoOperation(CreateOperation(created_object))
            UndoRedoService.clear_redo()
        
        return created_object
        
    return wrapper
