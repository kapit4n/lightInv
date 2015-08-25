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


class User(Employee):
    def __init__(self, display_name, email, login, password, user_type, id=0):
        Employee.__init__(self, display_name)
        self.display_name = display_name
        self.email = email
        self.login = login
        self.password = password
        self.user_type = user_type
        self.id = id
        self.name = display_name

    def fields(self):
        return 'display_name, email, login, password, user_type'

    def values(self):
        return "'{0}', '{1}', '{2}', '{3}', '{4}'"\
            .format(self.display_name, self.email, self.login, self.password,
                    self.user_type)

    def tableName(self):
        return "user"

    def updateValues(self):
        return "display_name= '{0}', email= '{1}', login= '{2}',"\
            "password= '{3}', user_type= '{4}'"\
            .format(self.display_name, self.email, self.login, self.password,
                    self.user_type)

    def setValues(self, cursor):
        for (display_name, email, login, password, user_type) in cursor:
            self.display_name = display_name
            self.email = email
            self.login = login
            self.password = password
            self.user_type = user_type

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass

    @staticmethod
    def getList(db):
        query = "select id, display_name, email, login, password, user_type from user"
        users = []
        for (id, display_name, email, login, password, user_type) in db.executeQuery(query):
            users.append(User(display_name, email, login, password,
                              user_type, id))
        return users
