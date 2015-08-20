import abc
from model.product import *
from model.delivery import *
from queue import *


class Employee(IQueryable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def create(self, name):
        pass

    def fields(self):
        return 'driver'

    def values(self):
        return "'{0}'".format(self.name)

    def tableName(self):
        return "storekeeper"

    def updateValues(self):
        return "name= '{0}'".format(self.name + ' Updated')

    def setValues(self, cursor):
        for (name) in cursor:
                self.name = name

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass


class Driver(Employee):
    def __init__(self, name, id=0):
        Employee.__init__(self, name)
        self.id = id

    def drive(self):
        pass

    def fields(self):
        return 'name'

    def values(self):
        return "'{0}'".format(self.name)

    def tableName(self):
        return "driver"

    def updateValues(self):
        return "name= '{0}'".format(self.name + ' Updated')

    def setValues(self, cursor):
        for (hello) in cursor:
                self.name = hello

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass

    @staticmethod
    def getList(db):
        query = "select id, name from driver"
        drivers = []
        for (id, name) in db.executeQuery(query):
            drivers.append(Driver(name, id))
        return drivers


class Storekeeper(Employee):
    def __init__(self, name, id=0):
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

    def fields(self):
        return 'name'

    def values(self):
        return "'{0}'".format(self.name)

    def tableName(self):
        return "storekeeper"

    def updateValues(self):
        return "name= '{0}'".format(self.name + ' Updated')

    def setValues(self, cursor):
        for (name) in cursor:
                self.name = name

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass
