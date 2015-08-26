from flask import Flask, session, render_template, url_for, redirect
import datetime
from flask import request
from utils.queries import DBManager
from model.product import Product
from model.delivery import PackageDelivery, Address
from model.employee import User, Driver
from utils.roles import UserManager

app = Flask(__name__)
app.secret_key = 'mySecretKey'


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter


@app.route("/")
def template_test():
    return render_template('template.html', my_string="Wheeeee!",
                           my_list=[0, 1, 2, 3, 4, 5], title="Index",
                           current_time=datetime.datetime.now())


@app.route('/product', methods=['POST', 'GET'])
def product():
    if validUser() != '':
        return validUser()

    db = DBManager()
    if request.method == 'POST':
        product = Product(request.form['name'], request.form['code1'],
                          request.form['quantity'])
        product.save(DBManager())
        return redirect("/product")
    else:
        products = Product.getList(db)
        return render_template('products.html', my_string="Bar",
                               title="Products",
                               current_time=datetime.datetime.now(),
                               products=products, userMenu=getUserRoles())


@app.route('/login', methods=['POST', 'GET'])
def login():
    db = DBManager()
    if request.method == 'POST':
        user = User.login(db, request.form['login'], request.form['password'])
        if user is not None:
            session['user'] = user.display_name
            session['userId'] = user.id
            session['user_type'] = user.user_type
            return redirect(UserManager.getInititalPage(user.user_type))
        else:
            return redirect("/login")
    else:
        return render_template('login.html', title="Login User")


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'user' not in session:
        return redirect(url_for('login'))

    session.pop('user', None)
    return redirect('/')


@app.route('/quick', methods=['POST', 'GET'])
def quick():
    if validUser() != '':
        return validUser()
    db = DBManager()
    if request.method == 'POST':
        product = Product(request.form['name'])
        product.save(DBManager())
        return redirect("/product")
    else:
        packageIdAux = 0
        if request.args.get('packageId') is not None:
            packageIdAux = request.args.get('packageId')
        products = Product.getList(db)

        return render_template('storekeeper.html', my_string="Bar",
                               title="Store Keeper",
                               current_time=datetime.datetime.now(),
                               products=products, packageId=packageIdAux,
                               userMenu=getUserRoles())


@app.route('/create-package', methods=['POST'])
def createPackage():
    if validUser() != '':
        return validUser()
    db = DBManager()
    packageId = 0

    if request.form['packageId'] is not None:
        packageId = request.form['packageId']
    productIds = []
    products = []
    for productId in request.values.getlist('productId'):
        productIds.append(productId)

    if len(productIds) > 0:
        products = Product.getList(db, ",".join(productIds))
        if len(products) > 0:
            for p in products:
                if request.form['productQuantity-' + str(p.id)] is '':
                    p.quantity = 0
                else:
                    p.quantity = int(request.form['productQuantity-' + str(p.id)])

    package = PackageDelivery(products, session['userId'])
    package.id = int(packageId)
    if package.id > 0:
        package.saveChilds(db)
    else:
        package.save(db, True)

    return redirect("/manage-package/" + str(package.id))


@app.route('/update-package/<packageId>', methods=['POST'])
def updatePackage(packageId):
    if validUser() != '':
        return validUser()
    db = DBManager()
    package = PackageDelivery([], request.form['addressId'],
                              request.form['driverId'])
    package.id = request.form['packageId']
    package.save(db)
    return redirect("/manage-package/" + str(package.id))


@app.route('/update-driver', methods=['POST'])
def updateDriver():
    if validUser() != '':
        return validUser()
    db = DBManager()
    package = PackageDelivery()
    package.driver = request.form['driverId']
    package.customer = request.form['customerId']
    package.id = request.form['packageId']
    package.save(db)
    return redirect("/manage-package/" + str(package.id))


@app.route('/update-customer', methods=['POST'])
def updateCustomer():
    if validUser() != '':
        return validUser()
    db = DBManager()
    package = PackageDelivery()
    package.customer = request.form['customerId']
    package.id = request.form['packageId']
    package.save(db)
    return redirect("/manage-package/" + str(package.id))


@app.route('/manage-package/<packageId>', methods=['GET'])
def managePackage(packageId):
    if validUser() != '':
        return validUser()
    db = DBManager()
    packageAux = PackageDelivery([])
    packageAux.id = packageId
    packageAux.pull(db)
    driverList = User.getListByType(db, 'driver')
    customers = User.getListByType(db, 'customer')
    workflows = UserManager.getWorkflows(session['user_type'],
                                         packageAux.status)

    return render_template('manage-package.html',
                           title="Package Administrator",
                           package=packageAux, drivers=driverList,
                           customers=customers, userMenu=getUserRoles(),
                           workflows=workflows)


@app.route('/review-package/<packageId>', methods=['GET'])
def reviewPackage(packageId):
    if validUser() != '':
        return validUser()
    db = DBManager()
    packageAux = PackageDelivery([])
    packageAux.id = packageId
    packageAux.pull(db)
    driverList = Driver.getList(db)
    addressListAux = Address.getList(db)
    return render_template('manage-package.html',
                           title="Package Administrator",
                           package=packageAux, drivers=driverList,
                           addressList=addressListAux, userMenu=getUserRoles())


@app.route('/package', methods=['GET'])
def package():
    if validUser() != '':
        return validUser()
    db = DBManager()
    packageList = PackageDelivery.getListByOwner(db, session['userId'])
    return render_template('package.html', title="Package Administrator",
                           packages=packageList, userMenu=getUserRoles())


@app.route('/customer', methods=['GET'])
def customer():
    if validUser() != '':
        return validUser()
    db = DBManager()
    packageList = PackageDelivery.getListByType(db, session['userId'],
                                                session['usert_type'])
    return render_template('customer.html', title="Customer",
                           packages=packageList, userMenu=getUserRoles())


@app.route('/driver', methods=['GET'])
def driver():
    if validUser() != '':
        return validUser()
    db = DBManager()
    packageList = PackageDelivery.getListByType(db, session['userId'],
                                                session['user_type'])
    return render_template('customer.html', title="Customer",
                           packages=packageList, userMenu=getUserRoles())


@app.route('/save-package', methods=['POST'])
def savePackage():
    pass


@app.route('/start', methods=['POST'])
def start():
    return ''


@app.route('/user', methods=['POST', 'GET'])
def user():
    if validUser() != '':
        return validUser()
    db = DBManager()
    if request.method == 'POST':
        user = User(request.form['display_name'], request.form['email'],
                    request.form['login'], request.form['password'],
                    request.form['user_type'])
        user.save(db)
        return redirect("/user")
    else:
        users = User.getList(db)
        return render_template('user.html', title="Users", users=users,
                               userMenu=getUserRoles())


def validUser():
    if 'user' in session:
        if session['user'] is not None:
            return ''
    return redirect(url_for('login'))


def getUserRoles():
    return UserManager.getMenuByUserType(session['user_type'])

if __name__ == '__main__':
    app.run(debug=True)
