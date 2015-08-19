import abc
from utils.queries import *


class AbstractProduct(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name


class Coke(AbstractProduct, IQueryable):
    def __init__(self, name, id=0):
        AbstractProduct.__init__(self, name)
        self.type = "Coke"
        self.id = id

    def fields(self):
        return 'name'

    def values(self):
        return "'{0}'".format(self.name)

    def tableName(self):
        return "Coke"

    def updateValues(self):
        return "name= '{0}'".format(self.name + ' Updated')

    def setValues(self, cursor):
        for (name) in cursor:
                self.name = name


class Fanta(AbstractProduct, IQueryable):
    def __init__(self, name, id=0):
        AbstractProduct.__init__(self, name)
        self.id = id
        self.type = "Fanta"

    def fields(self):
        return "name"

    def values(self):
        return "'{0}'".format(self.name)

    def tableName(self):
        return "Fanta"

    def updateValues(self):
        return "name= '{0}'".format(self.name + ' Updated')

    def setValues(self, cursor):
        for (name) in cursor:
                self.name = name
