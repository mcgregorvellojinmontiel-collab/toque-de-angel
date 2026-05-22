from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from werkzeug.utils import secure_filename

import os

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'MYSQL_PUBLIC_URL'
)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text)

    price = db.Column(db.Float, nullable=False)

    image = db.Column(db.String(255))

    active = db.Column(db.Boolean, default=True)


@app.route('/')
def home():

    products = Product.query.filter_by(active=True).all()

    return render_template(
        'index.html',
        products=products
    )


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form.get('username')

        password = request.form.get('password')

        admin_user = os.getenv('ADMIN_USER')

        admin_password = os.getenv('ADMIN_PASSWORD')

        if username == admin_user and password == admin_password:

            session['admin'] = True

            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/admin/delete-product/<int:id>')
def delete_product(id):

    if not session.get('admin'):

        return redirect(url_for('admin_login'))

    product = Product.query.get_or_404(id)

    db.session.delete(product)

    db.session.commit()

    return redirect(url_for('dashboard'))



@app.route('/admin/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):

    if not session.get('admin'):

        return redirect(url_for('admin_login'))

    product = Product.query.get_or_404(id)

    if request.method == 'POST':

        product.name = request.form.get('name')

        product.description = request.form.get('description')

        product.price = request.form.get('price')

        image = request.files.get('image')

        if image and image.filename != '':

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

            product.image = f'/static/uploads/{filename}'

        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template(
        'edit_product.html',
        product=product
    )



@app.route('/admin/dashboard')
def dashboard():

    if not session.get('admin'):

        return redirect(url_for('admin_login'))

    products = Product.query.all()

    return render_template(
        'dashboard.html',
        products=products
    )


@app.route('/admin/create-product', methods=['GET', 'POST'])
def create_product():

    if not session.get('admin'):

        return redirect(url_for('admin_login'))

    if request.method == 'POST':

        name = request.form.get('name')

        description = request.form.get('description')

        price = request.form.get('price')

        image = request.files.get('image')

        filename = ''

        if image and image.filename != '':

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

        product = Product(
            name=name,
            description=description,
            price=price,
            image=f'/static/uploads/{filename}'
        )

        db.session.add(product)

        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('create_product.html')


@app.route('/admin/logout')
def logout():

    session.clear()

    return redirect(url_for('admin_login'))


if __name__ == '__main__':

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.app_context():
        db.create_all()
        print("TABLES CREATED")

    app.run(debug=True)
