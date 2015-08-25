from utils.queries import *
from model.product import *
import datetime


class PackageDelivery(IQueryable):

    def __init__(self, products, owner=0, customer=0, destiny=0, driver=0, status='new', id=0):
        self.created_at = datetime.datetime.now()
        self.packageItems = []
        for product in products:
            self.packageItems.append(PackageItem(id, product.id, product.name, product.quantity))
        self.products = products
        self.owner = owner
        self.customer = customer
        self.driver = driver
        self.destiny = destiny
        self.id = id
        self.status = status
        self.name = "Package ({0}, {1}, {2})".format(self.created_at, self.destiny, self.driver)

    def fields(self):
        return "created_at, owner, customer, destiny, driver_id, status "

    def values(self):
        return "'{0}', '{1}', '{2}', '{3}', '{4}', '{5}'".format(self.created_at, self.owner, self.customer, self.destiny, self.driver, self.status)

    def tableName(self):
        return "package"

    def updateValues(self):
        return "driver_id= '{0}', destiny= '{1}'".format(self.driver, self.destiny)

    def updateStatusValue(self):
        return "status= '{0}'".format(self.status)

    def setValues(self, cursor):
        for (created_at, owner, self.customer, destiny, driver_id, status) in cursor:
            self.created_at = created_at
            self.owner = owner
            self.customer = customer
            self.destiny = destiny
            self.driver = driver_id
            self.status = status

    def saveChilds(self, db):
        for item in self.packageItems:
            item.packageId = self.id
            item.save(db)

    def pullChildren(self, db):
        childrenFields = "id, package_id, product_id, product_name, quantity"
        childTable = "package_item"
        queryFormat = "select {0} from {1} where package_id = {2}"
        query = queryFormat.format(childrenFields, childTable, self.id)
        self.packageItems = []
        for (id, package_id, product_id, product_name, quantity) in db.executeQuery(query):
            self.packageItems.append(PackageItem(package_id, product_id, product_name, quantity, id))

    @staticmethod
    def getList(db):
        query = "select id, created_at, owner, customer, destiny, driver_id, status from package"
        packageList = []
        for (id, created_at, owner, customer, destiny, driver_id, status) in db.executeQuery(query):
            packageList.append(PackageDelivery([], owner, customer, destiny, driver_id, status, id))
        return packageList

    @staticmethod
    def getListByOwner(db, ownerId):
        query = "select id, created_at, owner, customer, destiny, driver_id, status from package where owner='{0}'".format(ownerId)
        packageList = []
        for (id, created_at, owner, customer, destiny, driver_id, status) in db.executeQuery(query):
            packageList.append(PackageDelivery([], owner, customer, destiny, driver_id, status, id))
        return packageList

    @staticmethod
    def getListByCustomer(db, ownerId):
        query = "select id, created_at, owner, customer, destiny, driver_id, status from package where customer='{0}'".format(ownerId)
        packageList = []
        for (id, created_at, owner, customer, destiny, driver_id, status) in db.executeQuery(query):
            packageList.append(PackageDelivery([], owner, customer, destiny, driver_id, status, id))
        return packageList


class PackageItem(IQueryable):
    def __init__(self, packageId, productId, productName, quantity=0, id=0):
        self.productId = productId
        self.productName = productName
        self.quantity = quantity
        self.id = id
        self.packageId = packageId

    def fields(self):
        return "package_id, product_id, product_name, quantity"

    def values(self):
        return "{0},{1},'{2}','{3}'".format(self.packageId, self.productId, self.productName, self.quantity)

    def tableName(self):
        return "package_item"

    def updateValues(self):
        return "package_id = {0}, product_id= {1}, product_name= '{2}', quantity= '{3}'".format(self.productId, self.productName, self.quantity)

    def setValues(self, cursor):
        for (package_id, product_id, product_name, quantity) in cursor:
            self.productId = product_id
            self.productName = product_name
            self.packageId = package_id
            self.quantity = quantity

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass


class Address(IQueryable):
    def __init__(self, city, street, number, id=0):
        self.city = city
        self.street = street
        self.number = number
        self.id = id
        self.name = "{0} {1} {2}".format(self.city, self.street, self.number)

    def fields(self):
        return "city, street, number"

    def values(self):
        return "'{0}', '{1}', {2}".format(self.city, self.street, self.number)

    def tableName(self):
        return "address"

    def updateValues(self):
        return "city= '{0}', street= '{1}', number= {2}".format(self.city, self.street, self.number)

    def setValues(self, cursor):
        for (name) in cursor:
                self.name = name

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass

    @staticmethod
    def getList(db):
        query = "select id, city, street, number from address"
        addressList = []
        for (id, city, street, number) in db.executeQuery(query):
            addressList.append(Address(city, street, number, id))
        return addressList


class Car(IQueryable):
    def __init__(self, model, capacity, type, id=0):
        self.model = model
        self.capacity = capacity
        self.type = type
        self.id = id

    def fields(self):
        return "model, capacity, type"

    def values(self):
        return "'{0}', {1}, '{2}'".format(self.model, self.capacity, self.type)

    def tableName(self):
        return "car"

    def updateValues(self):
        return "model= '{0}', capacity= {1}, type= '{2}'".format(self.model, self.capacity, self.type)

    def setValues(self, cursor):
        for (name) in cursor:
                self.name = name

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass
