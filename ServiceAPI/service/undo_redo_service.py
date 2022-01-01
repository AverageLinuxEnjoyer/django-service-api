from ..UndoRedoOperations.undo_redo_operation import UndoRedoOperation


class UndoRedoService:
    undo_list: list[UndoRedoOperation] = []
    redo_list: list[UndoRedoOperation] = []

    def undo():
        if UndoRedoService.undo_list:
            print("Undo done.")
            top_operation = UndoRedoService.undo_list.pop()
            top_operation.undo()
            UndoRedoService.redo_list.append(top_operation)

            return "Success"
        else:
            return "Failure"

    def redo():
        if UndoRedoService.redo_list:
            print("Redo done.")
            top_operation = UndoRedoService.redo_list.pop()
            top_operation.redo()
            UndoRedoService.undo_list.append(top_operation)

            return "Success"
        else:
            return "Failure"

    def clear_redo():
        UndoRedoService.redo_list.clear()

    def addUndoOperation(operation: UndoRedoOperation):
        UndoRedoService.undo_list.append(operation)
        print("Undo operation added.")
