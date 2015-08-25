
from utils.queries import IQueryable


class Product(IQueryable):
    def __init__(self, name, code, quantity=0, id=0):
        self.name = name
        self.code = code
        self.quantity = quantity
        self.id = id

    def fields(self):
        return 'name, code, quantity'

    def values(self):
        return "'{0}','{1}','{2}'".format(self.name, self.code, self.quantity)

    def tableName(self):
        return "product"

    def updateValues(self):
        return "name= '{0}', code= '{1}', quantity= '{2}'"\
            .format(self.name, self.code, self.quantity)

    def setValues(self, cursor):
        for (name, code, quantity) in cursor:
            self.name = name
            self.code = code
            self.quantity = quantity

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass

    @staticmethod
    def getList(db, ids=None):
        if ids is None:
            query = "select id, name, code, quantity from product"
        else:
            query = "select id, name, code, quantity from product "\
                " where id in ({0})".format(ids)
        products = []
        for (id, name, code, quantity) in db.executeQuery(query):
            products.append(Product(name, code, quantity, id))
        return products
