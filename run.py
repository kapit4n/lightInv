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
        if request.form['productType'] == "Fanta":
            product = Fanta(request.form['name'])
        else:
            product = Coke(request.form['name'])
        product.save(DBManager())
        return redirect("/product")
    else:
        products = []
        for(id, name) in db.executeQuery("Select id, name from Fanta"):
            products.append(Fanta(name, id))

        for(id, name) in db.executeQuery("Select id, name from Coke"):
            products.append(Coke(name, id))

        return render_template('products.html', my_string="Bar",
            title="Products", current_time=datetime.datetime.now(),
            products=products, productTypes=['Fanta', 'Coke'])


@app.route('/home', methods=['POST', 'GET'])
def home():
    db = DBManager()
    if request.method == 'POST':
        print(request.form)
        product = None
        if request.form['productType'] == "Fanta":
            product = Fanta(request.form['name'])
        else:
            product = Coke(request.form['name'])
        product.save(DBManager())
        return redirect("/product")
    else:
        products = []
        for(id, name) in db.executeQuery("Select id, name from Fanta"):
            products.append(Fanta(name, id))

        for(id, name) in db.executeQuery("Select id, name from Coke"):
            products.append(Coke(name, id))

        return render_template('storekeeper.html', my_string="Bar",
            title="Store Keeper", current_time=datetime.datetime.now(), 
            products=products, productTypes=['Fanta', 'Coke'])


@app.route("/contact")
def contact():
    return render_template('template.html', my_string="FooBar",
        my_list=[18, 19, 20, 21, 22, 23], title="Contact Us", current_time=datetime.datetime.now())


@app.route('/create-package', methods=['POST'])
def createPackage():
    db = DBManager()
    fantas = []
    cokes = []
    for product in request.values.getlist('productId'):
        if product.split('-')[1] == 'Fanta':
            fantas.append(product.split('-')[0])
        else:
            cokes.append(product.split('-')[0])
    products = []
    query = "Select id, name from Fanta where id in (" + ",".join(fantas) + ")"
    print(query)
    for(id, name) in db.executeQuery(query):
            products.append(Fanta(name, id))

    package = PackageDelivery(products)
    package.save(db)
    return redirect("/manage-package/" + str(package.id))


@app.route('/update-package', methods=['PUT'])
def updatePackage():
    db = DBManager()
    fantas = []
    cokes = []
    for product in request.values.getlist('productId'):
        print("FFFFFFFFFFFFFFFFFFF " + product)
        if product.split('-')[1] == 'Fanta':
            fantas.append(product.split('-')[0])
        else:
            cokes.append(product.split('-')[0])
    products = []

    query = "Select id, name from Fanta where id in (" + ",".join(fantas) + ")"

    for(id, name) in db.executeQuery(query):
            products.append(Fanta(name, id))
    query = "Select id, name from Fanta where id in (" + ",".join(cokes) + ")"
    for(id, name) in db.executeQuery(query):
            products.append(Coke(name, id))
    package = PackageDelivery(products)
    package.save(db)
    return redirect("/manage-package/" + str(package.id))


@app.route('/manage-package/<packageId>', methods=['GET'])
def managePackage(packageId):
    db = DBManager()
    fantas = []
    cokes = []
    packageAux = PackageDelivery([])
    packageAux.id = packageId
    packageAux.pull(db)
    driverList = Driver.getList(db)
    return render_template('package.html', title="Package Administrator", package=packageAux, drivers=driverList)


@app.route('/save-package', methods=['PUT'])
def savePackage():
    return "Package saved"


@app.route('/driver', methods=['POST', 'GET'])
def driver():
    db = DBManager()
    if request.method == 'POST':
        driver = Driver(request.form['name'])
        driver.save(DBManager())
        return redirect("/driver")
    else:
        drivers = Driver.getList(db)
        return render_template('driver.html', title="Drivers", drivers=drivers)


if __name__ == '__main__':
    app.run(debug=True)
