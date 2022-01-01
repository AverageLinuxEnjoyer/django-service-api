from .car_service import CarService
from .card_service import CardService

def full_text_search(text: str):
    return (
        CarService.search(text),
        CardService.search(text)
    )