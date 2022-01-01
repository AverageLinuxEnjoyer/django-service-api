from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models.car import Car
from ..serializers.car_serializer import CarSerializer
from ..service.car_service import CarService



@api_view(['GET'])
def carOverview(request):
    api_urls = {
        'List': '/list/',
        'List decresing by workmanship': '/listByWorkmanship/',
        'Detail View': '/detail/<str:pk>/',
        'Create': '/create/',
        'Create n random': '/random/<int:n>/',
        'Update': '/update/<str:pk>/',
        'Renew warranty': '/renewWarranty/',
        'Delete': '/delete/<str:pk>/',
    }

    return Response(api_urls)


@api_view(['GET'])
def carList(request):
    cars = CarService.getAll()
    serializer = CarSerializer(instance=cars, many=True)

    return Response(data=serializer.data)


@api_view(['GET'])
def carListDecreasingByWorkmanship(request):
    cars = CarService.getAllDecreasingByWorkmanship()
    serializer = CarSerializer(instance=cars, many=True)

    return Response(data=serializer.data)


@api_view(['GET'])
def carDetail(request, pk):
    try:
        car = CarService.get(id=pk)
    except Car.DoesNotExist as e:
        return Response(data={"detail": str(e)})

    serializer = CarSerializer(instance=car, many=False)
    return Response(data=serializer.data)


@api_view(['POST'])
def carCreate(request):
    serializer = CarSerializer(data=request.data)

    if serializer.is_valid():
        car = CarService.create(car=serializer.create())
        return Response(data=CarSerializer(instance=car, many=False).data)
    else:
        return Response(data=serializer.errors)


@api_view(['POST'])
def carCreateRandom(request, n):
    cars = CarService.createRandom(n)
    serializer = CarSerializer(instance=cars, many=True)

    return Response(data=serializer.data)


@api_view(['PUT'])
def carUpdate(request, pk):
    serializer = CarSerializer(data=request.data)

    if serializer.is_valid():
        car = CarService.update(id=pk, new_car=serializer.create())
        return Response(data=CarSerializer(instance=car, many=False).data)
    else:
        return Response(data=serializer.errors)


@api_view(['PUT'])
def carRenewWarranty(request):
    cars = CarService.renewWarranty()
    serializer = CarSerializer(instance=cars, many=True)

    return Response(data=serializer.data)


@api_view(['DELETE'])
def carDelete(request, pk):
    try:
        serializer = CarSerializer(
            instance=CarService.delete(id=pk), 
            many=False
        )
        return Response(data=({
            "detail":"success",
            "deleted_object:":serializer.data
        }))
    except Car.DoesNotExist as e:
        return Response(data={"detail": str(e)})
