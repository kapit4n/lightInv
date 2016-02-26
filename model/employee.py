import abc
from utils.queries import IQueryable


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
        return "name= '{0}'".format(self.name)

    def setValues(self, cursor):
        for (name) in cursor:
                self.name = name

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass


class User(Employee):
    def __init__(self, display_name, email='', login='', password='',
                 user_type='', id=0):
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
        query = "select id, display_name, email, login, password, user_type"\
            " from user where user_type != 'admin'"
        users = []
        qResult = db.executeQuery(query)
        for (id, display_name, email, login, password, user_type) in qResult:
            users.append(User(display_name, email, login, password,
                              user_type, id))
        return users

    @staticmethod
    def getListByType(db, user_type):
        query = "select id, display_name, email, login, password, user_type"\
            " from user where user_type='{0}'".format(user_type)
        users = []
        qResult = db.executeQuery(query)
        for (id, display_name, email, login, password, user_type) in qResult:
            users.append(User(display_name, email, login, password,
                              user_type, id))
        return users

    @staticmethod
    def login(db, login, password):
        query = "select id, display_name, user_type from user "\
            "where login='{0}' and password='{1}'"\
            .format(login, password)
        for(id, display_name, user_type) in db.executeQuery(query):
            user = User(display_name)
            user.user_type = user_type
            user.id = id
            return user
        return None

    @staticmethod
    def deleteUser(db, id):
        query = "delete from user where id='{0}'".format(id)
        db.deleteQuery(query)
