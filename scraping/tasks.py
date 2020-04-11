from celery import shared_task
from celery.utils.log import get_task_logger

# from catalog.models import Car

# from scraping.scrapers.drive2 import scrap_manufacturers
# from scraping.scrapers.google import scrap_images as scrap_google_images


logger = get_task_logger('scraping')


@shared_task(name='scrap_yahoo')
def scrap_yahoo():
    scrap_yahoo()

"""

@shared_task(name='scrap_drive2')
def scrap_drive2():
    scrap_manufacturers()


@shared_task(name='scrap_google')
def scrap_google():
    cars = Car.objects.order_by('?')[:5]
    for car in cars:
        scrap_google_images(car)
        
"""
