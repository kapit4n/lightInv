from utils.queries import *
from model.product import *
import datetime


class PackageDelivery(IQueryable):

    def __init__(self, products, destiny=None, driver=None, id=0):
        self.created_at = datetime.datetime.now()
        self.packageItems = []
        for product in products:
            self.packageItems.append(PackageItem(id, product.id, product.name))
        self.products = products
        self.driver = driver
        self.destiny = destiny
        self.id = id

    def fields(self):
        return "created_at"

    def values(self):
        return "'{0}'".format(self.created_at)

    def tableName(self):
        return "package"

    def updateValues(self):
        return "name= '{0}'".format(self.name + ' Updated')

    def setValues(self, cursor):
        for (name) in cursor:
                self.name = name

    def saveChilds(self, db):
        for item in self.packageItems:
            item.packageId = self.id
            item.save(db)

    def pullChildren(self, db):
        childrenFields = "id, package_id, product_id, product_name"
        childTable = "package_item"
        queryFormat = "select {0} from {1} where package_id = {2}"
        query = queryFormat.format(childrenFields, childTable, self.id)
        self.packageItems = []
        for (id, package_id, product_id, product_name) in db.executeQuery(query):
            self.packageItems.append(PackageItem(package_id, product_id, product_name, id))


class PackageItem(IQueryable):
    def __init__(self, packageId, productId, productName, id=0):
        self.productId = productId
        self.productName = productName
        self.id = id
        self.packageId = packageId

    def fields(self):
        return "package_id, product_id, product_name"

    def values(self):
        return "{0},{1},'{2}'".format(self.packageId, self.productId, self.productName)

    def tableName(self):
        return "package_item"

    def updateValues(self):
        return "package_id = {0}, product_id= {1}, product_name= '{2}'".format(self.productId, self.productName)

    def setValues(self, cursor):
        for (package_id, product_id, product_name) in cursor:
            self.productId = product_id
            self.productName = product_name
            self.packageId = package_id

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
