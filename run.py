from flask import Flask, render_template, url_for,redirect
import datetime
from flask import request
from utils.queries import DBManager
from model.product import *
from model.delivery import *
from model.employee import *

app = Flask(__name__)


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter


@app.route("/")
def template_test():
    return render_template('template.html', my_string="Wheeeee!",
        my_list=[0, 1, 2, 3, 4, 5], title="Index", current_time=datetime.datetime.now())


@app.route('/product', methods=['POST', 'GET'])
def product():
    db = DBManager()
    if request.method == 'POST':
        product = Product(request.form['name'], request.form['code1'], request.form['quantity'])
        product.save(DBManager())
        return redirect("/product")
    else:
        products = Product.getList(db)
        return render_template('products.html', my_string="Bar",
            title="Products", current_time=datetime.datetime.now(),
            products=products)


@app.route('/quick', methods=['POST', 'GET'])
def home():
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
            title="Store Keeper", current_time=datetime.datetime.now(), 
            products=products, packageId=packageIdAux)


@app.route("/contact")
def contact():
    return render_template('template.html', my_string="FooBar",
        my_list=[18, 19, 20, 21, 22, 23], title="Contact Us", current_time=datetime.datetime.now())


@app.route('/create-package', methods=['POST'])
def createPackage():
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

    package = PackageDelivery(products)
    package.id = int(packageId)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(packageId)
    if package.id > 0:
        package.saveChilds(db)
    else:
        package.save(db, True)

    return redirect("/manage-package/" + str(package.id))


@app.route('/update-package/<packageId>', methods=['POST'])
def updatePackage(packageId):
    db = DBManager()
    package = PackageDelivery([], request.form['addressId'], request.form['driverId'])
    package.id = request.form['packageId']
    package.save(db)
    return redirect("/manage-package/" + str(package.id))


@app.route('/manage-package/<packageId>', methods=['GET'])
def managePackage(packageId):
    db = DBManager()
    packageAux = PackageDelivery([])
    packageAux.id = packageId
    packageAux.pull(db)
    driverList = Driver.getList(db)
    addressListAux = Address.getList(db)
    return render_template('manage-package.html', title="Package Administrator", 
        package=packageAux, drivers=driverList, addressList=addressListAux)


@app.route('/package', methods=['GET'])
def package():
    db = DBManager()
    packageList = PackageDelivery.getList(db)
    return render_template('package.html', title="Package Administrator", 
        packages=packageList)


@app.route('/save-package', methods=['POST'])
def savePackage():
    pass


@app.route('/driver', methods=['POST', 'GET'])
def driver():
    db = DBManager()
    if request.method == 'POST':
        driver = Driver(request.form['name'])
        driver.save(db)
        return redirect("/driver")
    else:
        drivers = Driver.getList(db)
        return render_template('driver.html', title="Drivers", drivers=drivers)


@app.route('/user', methods=['POST', 'GET'])
def user():
    db = DBManager()
    if request.method == 'POST':
        user = User(request.form['display_name'], request.form['email'],
            request.form['login'], request.form['password'],
            request.form['user_type'])
        user.save(db)
        return redirect("/user")
    else:
        users = User.getList(db)
        return render_template('user.html', title="Users", users=users)


@app.route('/address', methods=['POST', 'GET'])
def address():
    db = DBManager()
    if request.method == 'POST':
        address = Address(request.form['city'], request.form['street'], request.form['number'])
        address.save(db)
        return redirect("/address")
    else:
        addressListAux = Address.getList(db)
        return render_template('address.html', title="Address List", addressList=addressListAux)


if __name__ == '__main__':
    app.run(debug=True)
