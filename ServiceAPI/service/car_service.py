from ..serializers.car_serializer import CarSerializer
from ..models.car import Car
from ..utility.date_and_time import random_date

from .undo_redo_service import UndoRedoService

from ..UndoRedoDecorators.create_decorator import create_undo_redo
from ..UndoRedoDecorators.update_decorator import update_undo_redo
from ..UndoRedoDecorators.random_create_decorator import random_create_undo_redo

from random import randint, choice
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class CarService:
    def getAll():
        return Car.objects.all()

    def getAllDecreasingByWorkmanship():
        return Car.objects.order_by('-total_workmanship')

    def get(id: int):
        try:
            car = Car.objects.get(id=id)
        except Car.DoesNotExist as e:
            raise Car.DoesNotExist(f'Error: {str(e)}')

        return car

    def search(text: str):
        from django.db.models import Q
        cars = Car.objects.filter(
            Q(model__icontains=text) |
            Q(acquisition_date__icontains=text) |
            Q(kilometers__icontains=text) |
            Q(total_workmanship__icontains=text)
        )
        
        return cars

    @create_undo_redo
    def create(car: Car, undoredo: bool = True) -> Car:
        car.save()
        return car

    @random_create_undo_redo
    def createRandom(n: int, undoredo: bool = True) -> list[Car]:
        possible_models = [
            'Tesla Model S', 'Tesla Model 3',
            'Tesla Model X', 'Tesla Model Y',
            'Audi e-tron GT quattro', 'Audi RS e-tron GT',
            'Audi A1', 'Audi A3 ',
            'BMW X5', 'BMW X6',
            'BMW Z4', 'BMW iX3',
            'Chevrolet Blazer', 'Chevrolet Equinox',
            'Chevrolet Trax', 'Chevrolet Tahoe',
            'Maserati Ghibli', 'Maserati Levante',
            'Maserati Quattroporte', 'Maserati MC20',
            'Porsche 718 Cayman', 'Porsche 911 Carrera',
            'Porsche 911 GT3', 'Porsche Taycan',
            'Volkswagen Golf ', 'Volkswagen Passat',
            'Volkswagen Polo', 'Volkswagen Tiguan',
        ]

        cars = []
        
        for i in range(n):
            cars.append(CarService.create(Car(
                model=choice(possible_models),
                acquisition_date=random_date(
                    date(2000, 1, 1), date(2022, 1, 1)),
                kilometers=randint(0, 400000),
                warranty=choice([True, False])
            ), undoredo=False))


        return cars

    @update_undo_redo
    def update(new_car, id, undoredo: bool = True):
        import copy
        
        try:
            car = Car.objects.get(id=id)
        except Car.DoesNotExist as e:
            raise Car.DoesNotExist(f'Error: {str(e)}')

        car.model = new_car.model
        car.acquisition_date = new_car.acquisition_date
        car.kilometers = new_car.kilometers
        car.warranty = new_car.warranty
        car.total_workmanship = new_car.total_workmanship

        car.save()

        return car

    def renewWarranty(undoredo: bool = True):
        cars = Car.objects.all()

        today = datetime.today()

        for car in cars:
            difference = relativedelta(today, car.acquisition_date)
            if difference.years < 3 and car.kilometers < 60000:
                car.warranty = True
                car.save()
                print(car.id, " si-a innoit garantia!")

        return cars

    def delete(id, undoredo: bool = True):
        import copy
        try:
            car = Car.objects.get(id=id)
            car_copy = copy.deepcopy(car)
            
            car.delete()
            
        except Car.DoesNotExist as e:
            raise Car.DoesNotExist(f'Error: {str(e)}')

        return car_copy
