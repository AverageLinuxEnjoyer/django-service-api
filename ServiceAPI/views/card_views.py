from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models.card import Card
from ..serializers.card_serializer import CardSerializer
from ..service.card_service import CardService



@api_view(['GET'])
def cardOverview(request):
    api_urls = {
        'List': '/list/',
        'List decreasing by discount': '/listByDiscount/',
        'Detail View': '/detail/<str:pk>/',
        'Create': '/create/',
        'Create n random': '/random/<int:n>/',
        'Update': '/update/<str:pk>/',
        'Delete': '/delete/<str:pk>/',
    }

    return Response(api_urls)


@api_view(['GET'])
def cardList(request):
    cards = CardService.getAll()
    serializer = CardSerializer(instance=cards, many=True)

    return Response(data=serializer.data)


@api_view(['GET'])
def cardListDecreasingByDiscount(request):
    cards = CardService.getAllDecreasingByDiscount()
    serializer = CardSerializer(instance=cards, many=True)

    return Response(data=serializer.data)


@api_view(['GET'])
def cardDetail(request, pk):
    try:
        card = CardService.get(id=pk)
    except Card.DoesNotExist as e:
        return Response(data={"detail": str(e)})

    serializer = CardSerializer(instance=card, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def cardCreate(request):
    serializer = CardSerializer(data=request.data)

    if serializer.is_valid():
        card = CardService.create(card=serializer.create())
        return Response(data=CardSerializer(instance=card, many=False).data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
def cardCreateRandom(request, n):
    cards = CardService.createRandom(n)
    serializer = CardSerializer(instance=cards, many=True)
    return Response(data=serializer.data)


@api_view(['PUT'])
def cardUpdate(request, pk):
    serializer = CardSerializer(data=request.data)

    if serializer.is_valid():
        card = CardService.update(id=pk, new_card=serializer.create())
        return Response(data=CardSerializer(instance=card, many=False).data)
    else:
        return Response(data=serializer.errors)


@api_view(['DELETE'])
def cardDelete(request, pk):
    try:
        serializer = CardSerializer(
            instance=CardService.delete(id=pk), 
            many=False
        )
        return Response(data=serializer.data)
    except Card.DoesNotExist as e:
        return Response(data={"detail": str(e)})
