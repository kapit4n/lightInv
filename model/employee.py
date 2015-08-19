import abc
from model.product import *
from model.delivery import *
from queue import *


class Employee(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def create(self, name):
        pass


class Driver(Employee):
    def __init__(self, name):
        Employee.__init__(self, name)

    def drive(self):
        pass


class Storekeeper(Employee):
    def __init__(self, name):
        Employee.__init__(self, name)
        self.packages = Queue()

    def buildInitialPackage(self):
        products = []
        products.append(Fanta("fanta"))
        products.append(Coke("coke"))
        dest = Address("main st", "1010")
        self.packages.put(PackageDelivery(products, dest))

    def createPachage(self, products, dest):
        res = PackageDelivery(products, dest)
        return res

    def enQueuePackage(self, package):
        self.packages.put(package)

    def deliverPackage(self):
        if not self.packages.empty():
            item = self.packages.get()
            self.packages.task_done()
            return item
        else:
            return None
