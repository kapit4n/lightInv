import abc
import mysql.connector


class DBManager:
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', host='localhost',
                                            database='coke')
        self.cursor = self.conn.cursor()

    def executeInsert(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.lastrowid

    def executeUpdate(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.lastrowid

    def executeQuery(self, query):
        self.cursor.execute(query)
        return self.cursor


class IQueryable(object):

    __metaclass__ = abc.ABCMeta

    def save(self, db, saveChilds=None):
        if self.id is 0:
            query = "insert into {0} ({1}) values({2})"\
                .format(self.tableName(), self.fields(), self.values()) 
            self.id = db.executeInsert(query)
            if saveChilds:
                self.saveChilds(db)
        else:
            query = "update {0} SET {1} where id={2}"\
                .format(self.tableName(), self.updateValues(), self.id)
            db.executeUpdate(query)
            if saveChilds:
                self.saveChilds(db)

    def pull(self, db):
        if self.id is not None:
            query = "select {0} from {1} where id={2}"\
                .format(self.fields(), self.tableName(), self.id)
            self.cursor = db.executeQuery(query)
            self.setValues(self.cursor)
            self.pullChildren(db)

    @abc.abstractmethod
    def fields(self):
        pass

    @abc.abstractmethod
    def values(self):
        pass

    @abc.abstractmethod
    def tableName(self):
        pass

    @abc.abstractmethod
    def updateValues(self):
        pass

    @abc.abstractmethod
    def setValues(self, cursor):
        pass

    @abc.abstractmethod
    def saveChilds(self, db):
        pass

    @abc.abstractmethod
    def pullChildren(self, db):
        pass
