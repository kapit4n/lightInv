from flask import Flask, render_template, url_for,redirect
import datetime
from flask import request
from utils.queries import DBManager
from model.product import *

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


@app.route("/home")
def home():
    return render_template('template.html', my_string="Foo",
        my_list = [6, 7, 8, 9, 10, 11], title="Home", current_time=datetime.datetime.now())

@app.route('/product', methods=['POST', 'GET'])
def product():
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

        return render_template('products.html', my_string="Bar",
            title="Products", current_time=datetime.datetime.now(), 
            products=products, productTypes=['Fanta', 'Coke'])


@app.route("/contact")
def contact():
    return render_template('template.html', my_string="FooBar",
        my_list=[18, 19, 20, 21, 22, 23], title="Contact Us", current_time=datetime.datetime.now())


if __name__ == '__main__':
    app.run(debug=True)
