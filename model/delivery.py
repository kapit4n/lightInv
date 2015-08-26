from utils.queries import IQueryable
import datetime
from model.product import Product


class PackageDelivery(IQueryable):

    def __init__(self, products=[], owner=0, customer=0, destiny=0, driver=0,
                 status='pending', id=0):
        self.created_at = datetime.datetime.now()
        self.packageItems = []
        for product in products:
            self.packageItems.append(PackageItem(id, product.id, product.name,
                                                 product.quantity, 0))
        self.products = products
        self.owner = owner
        self.customer = customer
        self.driver = driver
        self.destiny = destiny
        self.id = id
        self.status = status
        self.name = "Package ({0}, {1}, {2})"\
            .format(self.created_at, self.destiny, self.driver)

    def fields(self):
        return "created_at, owner, customer, destiny, driver_id, status "

    def values(self):
        return "'{0}', '{1}', '{2}', '{3}', '{4}', '{5}'"\
            .format(self.created_at, self.owner, self.customer, self.destiny,
                    self.driver, self.status)

    def tableName(self):
        return "package"

    def updateValues(self):
        updateSt = []
        if int(self.owner) > 0:
            updateSt.append("owner= '{0}'".format(self.owner))
        if int(self.customer) > 0:
            updateSt.append("customer= '{0}'".format(self.customer))
        if int(self.destiny) > 0:
            updateSt.append("destiny= '{0}'".format(self.destiny))
        if int(self.driver) > 0:
            updateSt.append("driver_id= '{0}'".format(self.driver))
        if self.status != 'new':
            updateSt.append("status= '{0}'".format(self.status))

        return ','.join(updateSt)

    def updateStatusValue(self):
        return "status= '{0}'".format(self.status)

    def setValues(self, cursor):
        for (created_at, owner, customer, destiny, driver_id, status) in cursor:
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
        childrenFields = "id, package_id, product_id, product_name, quantity, quantity_filled"
        childTable = "package_item"
        queryFormat = "select {0} from {1} where package_id = {2}"
        query = queryFormat.format(childrenFields, childTable, self.id)
        self.packageItems = []
        for (id, package_id, product_id, product_name, quantity, quantity_filled) in db.executeQuery(query):
            self.packageItems.append(PackageItem(package_id, product_id,
                                                 product_name, quantity, quantity_filled, id))

    def fillPackage(self, db):
        products = {}
        for product in Product.getList(db):
            products[product.id] = product
        for item in self.packageItems:
            if item.quantity_filled <= item.quantity:
                item.fillPackageItem(products[item.productId])
                products[item.productId].save(db)
                item.save(db)

    def revertPackage(self, db):
        products = {}
        for product in Product.getList(db):
            products[product.id] = product
        for item in self.packageItems:
            if item.quantity_filled <= item.quantity:
                item.revertPackageItem(products[item.productId])
                products[item.productId].save(db)
                item.save(db)

    def isFilled(self):
        for item in self.packageItems:
            if item.quantity is not item.quantity_filled:
                return False
        return True

    def isFilledPartially(self):
        for item in self.packageItems:
            if item.quantity_filled > 0:
                return True
        return False

    @staticmethod
    def getList(db):
        query = "select id, created_at, owner, customer, destiny, driver_id, status from package"
        packageList = []
        for (id, created_at, owner, customer, destiny, driver_id, status) in db.executeQuery(query):
            packageList.append(PackageDelivery([], owner, customer, destiny, 
                                               driver_id, status, id))
        return packageList

    @staticmethod
    def getListByOwner(db, ownerId):
        query = "select id, created_at, owner, customer, destiny, driver_id, status from package where owner='{0}'".format(ownerId)
        packageList = []
        for (id, created_at, owner, customer, destiny, driver_id, status) in db.executeQuery(query):
            packageList.append(PackageDelivery([], owner, customer, destiny,
                                               driver_id, status, id))
        return packageList

    @staticmethod
    def getListByCustomer(db, ownerId):
        query = "select id, created_at, owner, customer, destiny, driver_id, status from package where customer='{0}'".format(ownerId)
        packageList = []
        for (id, created_at, owner, customer, destiny, driver_id, status) in db.executeQuery(query):
            packageList.append(PackageDelivery([], owner, customer, destiny,
                                               driver_id, status, id))
        return packageList

    @staticmethod
    def getListByType(db, ownerId, user_type):
        usertypeDict = {'customer': 'customer', 'storekeeper': 'owner',
                        'driver': 'driver_id'}
        query = "select id, created_at, owner, customer, destiny, driver_id,"\
            " status from package where {0}='{1}'"\
            .format(usertypeDict[user_type], ownerId)
        packageList = []
        for (id, created_at, owner, customer, destiny, driver_id, status) in db.executeQuery(query):
            packageList.append(PackageDelivery([], owner, customer, destiny,
                                               driver_id, status, id))
        return packageList


class PackageItem(IQueryable):
    def __init__(self, packageId, productId, productName, quantity=0,
                 quantity_filled=0, id=0):
        self.productId = productId
        self.productName = productName
        self.quantity = quantity
        self.id = id
        self.packageId = packageId
        self.quantity_filled = quantity_filled

    def fields(self):
        return "package_id, product_id, product_name, quantity, quantity_filled"

    def values(self):
        return "{0},{1},'{2}','{3}','{4}'"\
            .format(self.packageId, self.productId, self.productName,
                    self.quantity, self.quantity_filled)

    def tableName(self):
        return "package_item"

    def updateValues(self):
        return "product_id= '{0}', product_name= '{1}',"\
            "quantity= '{2}', quantity_filled= '{3}'"\
            .format(self.productId, self.productName, self.quantity,
                    self.quantity_filled)

    def setValues(self, cursor):
        for (package_id, product_id, product_name, quantity, quantity_filled) in cursor:
            self.productId = product_id
            self.productName = product_name
            self.packageId = package_id
            self.quantity = quantity
            self.quantity_filled = quantity_filled

    def fillPackageItem(self, product):
        productId = int(self.productId)
        if int(self.id) and productId > 0:
            if product.quantity >= (self.quantity - self.quantity_filled):
                product.quantity = product.quantity - self.quantity + self.quantity_filled
                self.quantity_filled = self.quantity
            else:
                self.quantity_filled = product.quantity + self.quantity_filled
                product.quantity = 0

    def revertPackageItem(self, product):
        if self.quantity_filled > 0:
            product.quantity = product.quantity + self.quantity_filled
            self.quantity_filled = 0

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
        return "model= '{0}', capacity= {1}, type= '{2}'"\
            .format(self.model, self.capacity, self.type)

    def setValues(self, cursor):
        for (name) in cursor:
                self.name = name

    def saveChilds(self, db):
        pass

    def pullChildren(self, db):
        pass


class PackageManager:
    statusNext = {'package': 'packaging', 'finishPackage': 'packaged',
                  'finish': 'closed', 'accept': 'accepted',
                  'abandon': 'abandoned', 'send': 'shipping',
                  'deliver': 'dispatched', 'pending': 'pending',
                  'reject': 'rejected', 'putOnHold': 'held'}

    @staticmethod
    def processWorkflow(package, status):
        return PackageManager.statusNext[status]

    @staticmethod
    def getWorkflows(userType, packageStatus):
        wfPackage = Workflow('package', 'Package')
        wfFinishPackage = Workflow('finishPackage', 'Finish Packaging')
        wfPutOnHold = Workflow('putOnHold', 'Put On Hold')
        wfShipping = Workflow('send', 'Send Package')
        wfDeliver = Workflow('deliver', 'Deliver')
        wfAccept = Workflow('accept', 'Accept')
        wfReject = Workflow('reject', 'Reject')
        wfPending = Workflow('pending', 'Pending')
        wfAbandon = Workflow('abandon', 'Abandon')
        wfFinish = Workflow('finish', 'Finish')

        sPending = [wfPutOnHold, wfPackage]
        sPackaging = [wfFinishPackage, wfAbandon]
        sPackaged = [wfShipping, wfAbandon]
        sShipping = [wfDeliver]
        sDelivered = [wfAccept, wfReject]
        sReject = [wfAbandon, wfPending]
        sAccepted = [wfFinish]
        sAbandoned = [wfFinish]
        sOnHold = [wfPending]

        storekeeper = {'pending': sPending, 'packaging': sPackaging,
                       'packaged': sPackaged, 'shipping': sShipping,
                       'dispatched': sDelivered, 'rejected': sReject,
                       'accepted': sAccepted, 'closed': [],
                       'abandoned': sAbandoned, 'held': sOnHold}

        customer = {'pending': [], 'packaging': [],
                    'packaged': [], 'shipping': [],
                    'dispatched': [sDelivered], 'rejected': [],
                    'accepted': [], 'closed': [],
                    'abandoned': [], 'held': []}

        driver = {'pending': [], 'packaging': [],
                  'packaged': [], 'shipping': sShipping,
                  'dispatched': [], 'rejected': [],
                  'accepted': [], 'closed': [],
                  'abandoned': [], 'held': []}

        workflows = {'customer': customer, 'driver': driver,
                     'storekeeper': storekeeper}
        return (workflows[userType])[packageStatus]


class Workflow:
    def __init__(self, action, name):
        self.name = name
        self.action = action
