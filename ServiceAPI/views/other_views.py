from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..service.undo_redo_service import UndoRedoService
from ..service.search import full_text_search

from ..serializers.card_serializer import CardSerializer
from ..serializers.car_serializer import CarSerializer

@api_view(['POST'])
def undo(request):
    return Response(UndoRedoService.undo())

@api_view(['POST'])
def redo(request):
    return Response(UndoRedoService.redo())

@api_view(['GET'])
def search(request):
    text = request.GET.get("text", "")
    
    cars, cards = full_text_search(text)

    car_serializer = CarSerializer(cars, many=True)
    card_serializer = CardSerializer(cards, many=True)

    return Response({
        "cars": car_serializer.data,
        "cards": card_serializer.data
    })
