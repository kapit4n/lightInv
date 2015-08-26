
class UserManager:
    @staticmethod
    def getMenuByUserType(userType):
        customer = [MenuItem('customer', 'HOME')]
        storekeeper = [MenuItem('quick', 'Quick Package'),
                       MenuItem('product', 'Product'),
                       MenuItem('user', 'Users'),
                       MenuItem('package', 'Package')]
        driver = [MenuItem('driver', 'HOME')]
        userMenus = {'customer': customer, 'storekeeper': storekeeper,
                     'driver': driver}

        return userMenus[userType]

    @staticmethod
    def getInititalPage(userType):
        customer = '/customer'
        storekeeper = '/quick'
        driver = '/driver'
        initialPage = {'customer': customer, 'storekeeper': storekeeper,
                       'driver': driver}

        return initialPage[userType]


class MenuItem:
    def __init__(self, dir, name):
        self.name = name
        self.dir = dir


