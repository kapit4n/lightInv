
class UserManager:
    @staticmethod
    def getMenuByUserType(userType):
        customer = [MenuItem('customer', 'HOME')]
        storekeeper = [MenuItem('quick', 'Quick Package'), MenuItem('product', 'Product'),
                       MenuItem('user', 'Users'), MenuItem('package', 'Package')]
        userMenus = {'customer': customer, 'storekeeper': storekeeper}
        return userMenus[userType]


class MenuItem:
    def __init__(self, dir, name):
        self.name = name
        self.dir = dir
