from utils.queries import *
from model.product import *
import datetime


class PackageDelivery:

    def __init__(self, products, destiny):
        self.created_at = datetime.datetime
        self.products = products
        self.destiny = destiny

    def createPackage(self):
        pass


class Address:
    def __init__(self, st, number):
        self.st = st
        self.number = number


class Car:
    def __init__(self, model, capacity):
        self.model = model
        self.capacity = capacity
