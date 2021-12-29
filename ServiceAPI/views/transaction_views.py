from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models.transaction import Transaction
from ..serializers.transaction_serializer import TransactionSerializer
from ..service.transaction_service import TransactionService

from ..models.car import Car


@api_view(['GET'])
def transactionOverview(request):
    api_urls = {
        'List': '/list/',
        'Detail View': '/detail/<str:pk>/',
        'List between sums': '/list/<str:start>/<str:end>/',
        'Create': '/create/',
        'Create n random': '/create/<int:n>/',
        'Update': '/update/<str:pk>/',
        'Delete': '/delete/<str:pk>/',
        'Delete between dates': '/delete/<str:start>/<str:end>/',

    }

    return Response(api_urls)


@api_view(['GET'])
def transactionList(request):
    transactions = TransactionService.getAll()
    serializer = TransactionSerializer(instance=transactions, many=True)

    return Response(data=serializer.data)


@api_view(['GET'])
def transactionDetail(request, pk):
    try:
        transaction = TransactionService.get(id=pk)
    except Transaction.DoesNotExist as e:
        return Response(data={"detail": str(e)})

    serializer = CarSerializer(instance=Car, many=False)
    return Response(data=serializer.data)


@api_view(['GET'])
def transactionBetweenSums(request, start, end):
    start = float(start)
    end = float(end)

    transactions = TransactionService.getBetweenSums(start, end)

    serializer = TransactionSerializer(transactions, many=True)
    return Response(data=serializer.data)


@api_view(['POST'])
def transactionCreate(request):
    serializer = TransactionSerializer(data=request.data)

    if serializer.is_valid():
        transaction = TransactionService.create(
            transaction=serializer.create())
        return Response(
            data=TransactionSerializer(
                instance=transaction,
                many=False)
            .data)
    else:
        return Response(data=serializer.errors)


@api_view(['POST'])
def transactionCreateRandom(request, n):
    try:
        transactions = TransactionService.createRandom(n)
    except Car.DoesNotExist as e:
        return Response(data={"detail": str(e)})

    serializer = TransactionSerializer(instance=transactions, many=True)
    return Response(data=serializer.data)


@api_view(['PUT'])
def transactionUpdate(request, pk):
    serializer = TransactionSerializer(data=request.data)

    if serializer.is_valid():
        transaction = TransactionService.update(
            id=pk,
            new_transaction=serializer.create()
        )
        return Response(data=TransactionSerializer(
            instance=transaction,
            many=False
        ).data)
    else:
        return Response(data=serializer.errors)


@api_view(['DELETE'])
def transactionDelete(request, pk):
    try:
        return Response(TransactionService.delete(id=pk))
    except Transaction.DoesNotExist as e:
        return Response(data={"detail": str(e)})


@api_view(['DELETE'])
def transactionDeleteBetweenDates(request, start, end):
    return Response(TransactionService.deleteBetweenDates(start, end))
